import os
import requests
import time
import pandas as pd
from dotenv import load_dotenv
import sys
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# Check if API key exists
if not API_KEY:
    print("Error: TMDB_API_KEY not found in environment variables.")
    print("Please add your API key to your .env file or environment variables.")
    sys.exit(1)

BASE_URL = "https://api.themoviedb.org/3"
DISCOVER_ENDPOINT = f"{BASE_URL}/discover/movie"
GENRE_ENDPOINT = f"{BASE_URL}/genre/movie/list"

def get_genres():
    url = GENRE_ENDPOINT
    params = {"api_key": API_KEY, "language": "en-US"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        genres_list = response.json().get("genres", [])
        return {genre["id"]: genre["name"] for genre in genres_list}
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Error: Invalid API key. Please check your TMDB_API_KEY.")
            print("You can get an API key from: https://www.themoviedb.org/settings/api")
        else:
            print(f"HTTP Error {response.status_code}: {e}")
        sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        print(f"Request error while fetching genres: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"Unexpected error while fetching genres: {e}")
        sys.exit(1)

def main():
    try:
        genres_map = get_genres()
    except SystemExit:
        return  # Exit gracefully if genre fetching failed

    titles = []
    years = []
    ratings = []
    descriptions = []
    genres = []

    per_page = 20
    target_movies = 10000
    max_pages = 500  # TMDb limit
    movies_fetched = 0

    print(f"TMDb Movie Scraper\nCopyright © 2025 Herald Inyang\n")
    print(f"Fetching up to {target_movies} movies across {max_pages} pages.\nPlease wait...")

    for page in range(1, max_pages + 1):
        params = {
            "api_key": API_KEY,
            "page": page,
            "sort_by": "popularity.desc",
            "include_adult": "true",
            "language": "en-US",
        }
        
        try:
            response = requests.get(DISCOVER_ENDPOINT, params=params)
            response.raise_for_status()
            data = response.json()
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print(f"\nError: Invalid API key. Please check your TMDB_API_KEY.")
                print("You can get an API key from: https://www.themoviedb.org/settings/api")
                break
            elif response.status_code == 429:
                print(f"\nRate limit exceeded. Waiting 10 seconds before retrying...")
                time.sleep(10)
                continue
            else:
                print(f"\nHTTP Error {response.status_code} on page {page}: {e}")
                print("Continuing with next page...")
                continue
        
        except requests.exceptions.RequestException as e:
            print(f"\nRequest error on page {page}: {e}")
            print("Continuing with next page...")
            continue
        
        except Exception as e:
            print(f"\nUnexpected error on page {page}: {e}")
            print("Continuing with next page...")
            continue
        
        results = data.get("results", [])
        if not results:
            print("\nNo more results.")
            break

        for movie in results:
            if movies_fetched >= target_movies:
                break
                
            titles.append(movie.get("title", ""))
            release_date = movie.get("release_date", "")
            year = release_date.split("-")[0] if release_date else ""
            years.append(year)
            ratings.append(movie.get("vote_average", 0))
            descriptions.append((movie.get("overview") or "").replace("\n", " ").strip())
            genre_names = [genres_map.get(gid, "") for gid in movie.get("genre_ids", [])]
            genres.append(", ".join(filter(None, genre_names)))

            movies_fetched += 1

        # Calculate and print percentage
        percentage_complete = (page / max_pages) * 100
        print(f"\r{percentage_complete:.2f}% complete", end="", flush=True)

        if movies_fetched >= target_movies:
            print(f"\nReached target of {target_movies} movies.")
            break
        time.sleep(0.25)

    if movies_fetched == 0:
        print("No movies were fetched. Please check your API key and internet connection.")
        return

    df = pd.DataFrame({
        "Title": titles,
        "Year": years,
        "Rating": ratings,
        "Description": descriptions,
        "Genre": genres,
    })

    print(f"\nScraped {len(df)} movies.")
    if len(df) < target_movies:
        print(f"⚠️ Note: {target_movies - len(df)} movie(s) skipped due to API limits.\n")
    
    try:
        df.to_csv("tmdb_movies.csv", index=False)
        print("Saved data to tmdb_movies.csv")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

if __name__ == "__main__":
    main()