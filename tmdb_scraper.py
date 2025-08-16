import os
import asyncio
import aiohttp
import time
import pandas as pd
from dotenv import load_dotenv
import sys
from tqdm.asyncio import tqdm
from typing import Dict, List, Tuple, Optional
import logging

load_dotenv()

# Configure logging for better error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = os.getenv("TMDB_API_KEY")

def env_bool(name: str, default: bool = False) -> bool:
    """Read env var into Python bool. Accepts 1/0, true/false, yes/no."""
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")
INCLUDE_ADULT = env_bool("TMDB_INCLUDE_ADULT", default=False)


# Check if API key exists
if not API_KEY:
    print("Error: TMDB_API_KEY not found in environment variables.")
    print("Please add your API key to your .env file or environment variables.")
    sys.exit(1)

BASE_URL = "https://api.themoviedb.org/3"
DISCOVER_ENDPOINT = f"{BASE_URL}/discover/movie"
GENRE_ENDPOINT = f"{BASE_URL}/genre/movie/list"

class TMDbScraperOptimized:
    def __init__(self, target_movies: int = 10000, concurrent_requests: int = 5):
        self.target_movies = target_movies
        self.concurrent_requests = concurrent_requests
        self.genres_map = {}
        self.movies_data = []
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(concurrent_requests)
        
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(
            limit=20,  # Connection pool size
            limit_per_host=10,  # Max connections per host
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': 'TMDb-Movie-Scraper/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def get_genres(self) -> Dict[int, str]:
        """Fetch movie genres with error handling"""
        params = {"api_key": API_KEY, "language": "en-US"}
        
        async with self.semaphore:
            try:
                async with self.session.get(GENRE_ENDPOINT, params=params) as response:
                    if response.status == 401:
                        raise Exception("Invalid API key. Please check your TMDB_API_KEY.")
                    
                    response.raise_for_status()
                    data = await response.json()
                    genres_list = data.get("genres", [])
                    return {genre["id"]: genre["name"] for genre in genres_list}
            
            except aiohttp.ClientError as e:
                logger.error(f"Request error while fetching genres: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error while fetching genres: {e}")
                raise

    async def fetch_page(self, page: int, retry_count: int = 3) -> Optional[List[Dict]]:
        """Fetch a single page of movies with retry logic"""
        params = {
            "api_key": API_KEY,
            "page": page,
            "sort_by": "popularity.desc",
            "language": "en-US",
        }

        # Only include adult flag if enabled
        if INCLUDE_ADULT:
            params["include_adult"] = str(INCLUDE_ADULT).lower()


        async with self.semaphore:
            for attempt in range(retry_count):
                try:
                    async with self.session.get(DISCOVER_ENDPOINT, params=params) as response:
                        if response.status == 401:
                            raise Exception("Invalid API key. Please check your TMDB_API_KEY.")
                        
                        if response.status == 429:  # Rate limit
                            wait_time = 2 ** attempt  # Exponential backoff
                            logger.warning(f"Rate limit hit on page {page}, waiting {wait_time}s...")
                            await asyncio.sleep(wait_time)
                            continue
                        
                        response.raise_for_status()
                        data = await response.json()
                        results = data.get("results", [])
                        
                        if not results:
                            logger.info(f"No results found for page {page}")
                            return None
                        
                        return results
                
                except aiohttp.ClientError as e:
                    logger.warning(f"Request error on page {page}, attempt {attempt + 1}: {e}")
                    if attempt == retry_count - 1:
                        logger.error(f"Failed to fetch page {page} after {retry_count} attempts")
                        return None
                    await asyncio.sleep(1 * attempt)  # Progressive delay
                
                except Exception as e:
                    logger.error(f"Unexpected error on page {page}: {e}")
                    return None
        
        return None

    def process_movie_data(self, movies: List[Dict]) -> List[Dict]:
        """Process raw movie data into clean format"""
        processed = []
        
        for movie in movies:
            # Stop if we've reached target
            if len(self.movies_data) >= self.target_movies:
                break
                
            title = movie.get("title", "")
            release_date = movie.get("release_date", "")
            year = release_date.split("-")[0] if release_date else ""
            rating = movie.get("vote_average", 0)
            description = (movie.get("overview") or "").replace("\n", " ").strip()
            
            # Process genres
            genre_names = [
                self.genres_map.get(gid, "") 
                for gid in movie.get("genre_ids", [])
            ]
            genres = ", ".join(filter(None, genre_names))
            
            # Adult flag
            adult_flag = bool(movie.get("adult", False))

            movie_dict = {
                "Title": title,
                "Year": year,
                "Rating": rating,
                "Description": description,
                "Genre": genres,
            }

            # Only add "Adult" key if INCLUDE_ADULT is True
            if INCLUDE_ADULT:
                movie_dict["Adult"] = adult_flag

            processed.append(movie_dict)
        
        return processed

    async def scrape_movies_batch(self, start_page: int, end_page: int) -> List[Dict]:
        """Scrape a batch of pages concurrently"""
        tasks = []
        
        for page in range(start_page, end_page + 1):
            task = self.fetch_page(page)
            tasks.append(task)
        
        # Execute all requests concurrently
        page_results = await asyncio.gather(*tasks)
        
        # Process results
        batch_movies = []
        for page_data in page_results:
            if page_data and len(self.movies_data) < self.target_movies:
                processed = self.process_movie_data(page_data)
                batch_movies.extend(processed)
                self.movies_data.extend(processed)
                
                # Early exit if target reached
                if len(self.movies_data) >= self.target_movies:
                    break
        
        return batch_movies

    async def scrape_all_movies(self) -> pd.DataFrame:
        """Main scraping method with optimized batching"""
        start_time = time.time()
        
        print(f"TMDb Movie Scraper (Optimized)\nCopyright © 2025 Herald Inyang\n")
        print(f"🚀 Starting optimized scraping of {self.target_movies} movies...")
        print(f"📊 Using {self.concurrent_requests} concurrent requests\n")
        
        # Fetch genres first
        try:
            self.genres_map = await self.get_genres()
            print(f"✅ Fetched {len(self.genres_map)} genres")
        except Exception as e:
            print(f"❌ Failed to fetch genres: {e}")
            return pd.DataFrame()
        
        # Calculate batching strategy
        max_pages = min(500, (self.target_movies // 20) + 10)  # TMDb pages have ~20 movies
        batch_size = self.concurrent_requests * 2  # Optimal batch size
        
        print(f"📄 Processing up to {max_pages} pages in batches of {batch_size}")
        
        # Process pages in batches
        with tqdm(total=self.target_movies, desc="Movies scraped", unit="movies", dynamic_ncols=True) as pbar:
            for batch_start in range(1, max_pages + 1, batch_size):
                batch_end = min(batch_start + batch_size - 1, max_pages)
                try:
                    batch_movies = await self.scrape_movies_batch(batch_start, batch_end)
                    pbar.update(len(batch_movies))

                    if len(self.movies_data) >= self.target_movies:
                        break

                except Exception as e:
                    pbar.clear()
                    logger.error(f"Error processing batch {batch_start}-{batch_end}: {e}")
                    pbar.refresh()
                    continue

        
        # Trim to exact target and create DataFrame
        self.movies_data = self.movies_data[:self.target_movies]
        df = pd.DataFrame(self.movies_data)
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ Successfully scraped {len(df)} movies in {elapsed_time:.2f} seconds")
        print(f"⚡ Average speed: {len(df)/elapsed_time:.1f} movies/second")
        
        return df

    def save_to_csv(self, df: pd.DataFrame, filename: str = "tmdb_movies.csv") -> bool:
        """Save DataFrame to CSV with error handling"""
        try:
            df.to_csv(filename, index=False)
            print(f"💾 Saved data to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving CSV file: {e}")
            return False

async def main():
    """Main async function"""
    try:
        async with TMDbScraperOptimized(target_movies=10000, concurrent_requests=8) as scraper:
            df = await scraper.scrape_all_movies()
            
            if not df.empty:
                scraper.save_to_csv(df)
                print(f"\n🎬 Scraping complete! Found {len(df)} movies.")
                if len(df) < scraper.target_movies:
                    skipped = scraper.target_movies - len(df)
                    plural = "s" if skipped != 1 else ""
                    print(f"\n⚠️ NOTE: {skipped:,} movie{plural} skipped due to API limits.\n")    
            
            else:
                print("❌ No movies were scraped. Please check your API key and connection.")
                
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Scraping failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop" in str(e).lower():
            print("⚠️ Async event loop issue detected. Try running in a standard Python shell instead of notebooks.")
        else:
            raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
