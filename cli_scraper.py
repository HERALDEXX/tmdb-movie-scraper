#!/usr/bin/env python3
"""
TMDb Movie Scraper - CLI Interface
A command-line interface for the optimized TMDb movie scraper.
"""

import asyncio
import click
import json
import sqlite3
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

# Import the optimized scraper class
from tmdb_scraper import TMDbScraperOptimized, logger


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """TMDb Movie Scraper - CLI Interface
    
    A powerful command-line tool to scrape movie data from The Movie Database (TMDb).
    """
    pass


@cli.command()
@click.option('--count', '-c', default=1000, help='Number of movies to scrape (default: 1000)')
@click.option('--output', '-o', default='tmdb_movies.csv', help='Output filename (default: tmdb_movies.csv)')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['csv', 'json', 'xlsx', 'sqlite'], case_sensitive=False),
              default='csv', help='Output format (default: csv)')
@click.option('--concurrent', default=8, help='Number of concurrent requests (default: 8)')
@click.option('--include-adult', is_flag=True, help='Include adult content')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress all output except errors')
def scrape(count: int, output: str, output_format: str, concurrent: int, 
           include_adult: bool, verbose: bool, quiet: bool):
    """Scrape movies from TMDb API"""
    
    if verbose and quiet:
        click.echo("Error: --verbose and --quiet cannot be used together", err=True)
        sys.exit(1)
    
    if not quiet:
        click.echo(f"🎬 Starting TMDb scraper...")
        click.echo(f"📊 Target movies: {count:,}")
        click.echo(f"📁 Output: {output} ({output_format.upper()})")
        click.echo(f"🚀 Concurrent requests: {concurrent}")
        if include_adult:
            click.echo("🔞 Including adult content")
        click.echo()
    
    try:
        # Run the async scraper
        df = asyncio.run(_run_scraper(count, concurrent, include_adult, verbose, quiet))
        
        if df.empty:
            click.echo("❌ No data scraped. Please check your API key.", err=True)
            sys.exit(1)
        
        # Save in requested format
        success = _save_data(df, output, output_format, quiet)
        
        if success and not quiet:
            click.echo(f"✅ Successfully scraped {len(df):,} movies!")
            if len(df) < count:
                skipped = count - len(df)
                plural = "s" if skipped != 1 else ""
                click.echo(f"\n⚠️ NOTE: {skipped:,} movie{plural} skipped due to API limits.\n")
            _show_summary(df)
        
    except KeyboardInterrupt:
        click.echo("\n⚠️ Scraping interrupted by user.")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('filename')
@click.option('--format', '-f', 'input_format',
              type=click.Choice(['csv', 'json', 'xlsx'], case_sensitive=False),
              help='Input format (auto-detected if not specified)')
def info(filename: str, input_format: Optional[str]):
    """Show information about a scraped dataset"""
    
    file_path = Path(filename)
    if not file_path.exists():
        click.echo(f"❌ File not found: {filename}", err=True)
        sys.exit(1)
    
    try:
        # Auto-detect format if not specified
        if not input_format:
            input_format = file_path.suffix.lower().lstrip('.')
            if input_format == 'xlsx':
                input_format = 'xlsx'
            elif input_format == 'json':
                input_format = 'json'
            else:
                input_format = 'csv'
        
        # Load the data
        if input_format == 'csv':
            df = pd.read_csv(filename)
        elif input_format == 'json':
            df = pd.read_json(filename)
        elif input_format == 'xlsx':
            df = pd.read_excel(filename)
        else:
            click.echo(f"❌ Unsupported format: {input_format}", err=True)
            sys.exit(1)
        
        click.echo(f"📊 Dataset Information for: {filename}")
        click.echo("=" * 50)
        _show_summary(df, detailed=True)
        
    except Exception as e:
        click.echo(f"❌ Error reading file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--from-format', type=click.Choice(['csv', 'json', 'xlsx'], case_sensitive=False),
              help='Input format (auto-detected if not specified)')
@click.option('--to-format', type=click.Choice(['csv', 'json', 'xlsx', 'sqlite'], case_sensitive=False),
              required=True, help='Output format')
def convert(input_file: str, output_file: str, from_format: Optional[str], to_format: str):
    """Convert between different data formats"""
    
    if not Path(input_file).exists():
        click.echo(f"❌ Input file not found: {input_file}", err=True)
        sys.exit(1)
    
    try:
        # Auto-detect input format if not specified
        if not from_format:
            from_format = Path(input_file).suffix.lower().lstrip('.')
            if from_format not in ['csv', 'json', 'xlsx']:
                from_format = 'csv'
        
        # Load the data
        if from_format == 'csv':
            df = pd.read_csv(input_file)
        elif from_format == 'json':
            df = pd.read_json(input_file)
        elif from_format == 'xlsx':
            df = pd.read_excel(input_file)
        
        # Save in new format
        success = _save_data(df, output_file, to_format)
        
        if success:
            click.echo(f"✅ Converted {len(df):,} movies from {from_format.upper()} to {to_format.upper()}")
        else:
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Conversion failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration and check API key"""
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")
    include_adult = os.getenv("TMDB_INCLUDE_ADULT", "false").lower()
    
    click.echo("🔧 Current Configuration")
    click.echo("=" * 30)
    
    if api_key:
        masked_key = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else "*" * len(api_key)
        click.echo(f"API Key: {masked_key}")
    else:
        click.echo("❌ API Key: Not found")
        click.echo("   Set TMDB_API_KEY in your .env file")
    
    click.echo(f"Include Adult: {include_adult}")
    click.echo()
    
    # Test API key
    if api_key:
        click.echo("🧪 Testing API connection...")
        try:
            import aiohttp
            import asyncio
            
            async def test_api():
                async with aiohttp.ClientSession() as session:
                    url = "https://api.themoviedb.org/3/genre/movie/list"
                    params = {"api_key": api_key}
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            return len(data.get("genres", []))
                        else:
                            return None
            
            genre_count = asyncio.run(test_api())
            if genre_count:
                click.echo(f"✅ API connection successful! Found {genre_count} genres.")
            else:
                click.echo("❌ API connection failed. Check your API key.")
                
        except Exception as e:
            click.echo(f"❌ API test failed: {e}")


async def _run_scraper(count: int, concurrent: int, include_adult: bool, 
                      verbose: bool, quiet: bool) -> pd.DataFrame:
    """Run the optimized scraper with CLI options"""
    
    # Set environment variable for adult content if specified
    if include_adult:
        import os
        os.environ["TMDB_INCLUDE_ADULT"] = "true"
    
    # Configure logging based on verbosity
    if quiet:
        logger.setLevel(logging.ERROR)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    async with TMDbScraperOptimized(target_movies=count, concurrent_requests=concurrent) as scraper:
        return await scraper.scrape_all_movies()


def _save_data(df: pd.DataFrame, filename: str, format_type: str, quiet: bool = False) -> bool:
    """Save DataFrame in the specified format"""
    
    try:
        if format_type.lower() == 'csv':
            df.to_csv(filename, index=False)
            
        elif format_type.lower() == 'json':
            df.to_json(filename, orient='records', indent=2)
            
        elif format_type.lower() == 'xlsx':
            df.to_excel(filename, index=False, engine='openpyxl')
            
        elif format_type.lower() == 'sqlite':
            # Create SQLite database
            conn = sqlite3.connect(filename)
            df.to_sql('movies', conn, if_exists='replace', index=False)
            conn.close()
            
        else:
            click.echo(f"❌ Unsupported format: {format_type}", err=True)
            return False
        
        if not quiet:
            click.echo(f"💾 Data saved to: {filename}")
        return True
        
    except Exception as e:
        click.echo(f"❌ Failed to save {format_type.upper()} file: {e}", err=True)
        return False


def _show_summary(df: pd.DataFrame, detailed: bool = False):
    """Show dataset summary information"""
    
    click.echo(f"📈 Dataset Summary:")
    click.echo(f"   Total movies: {len(df):,}")
    
    if 'Year' in df.columns:
        years = df['Year'].dropna()
        if not years.empty:
            click.echo(f"   Year range: {years.min()} - {years.max()}")
    
    if 'Rating' in df.columns:
        ratings = df['Rating'].dropna()
        if not ratings.empty:
            click.echo(f"   Average rating: {ratings.mean():.1f}")
            click.echo(f"   Rating range: {ratings.min():.1f} - {ratings.max():.1f}")
    
    if 'Genre' in df.columns:
        # Count unique genres
        all_genres = set()
        for genre_str in df['Genre'].dropna():
            genres = [g.strip() for g in str(genre_str).split(',')]
            all_genres.update(genres)
        all_genres.discard('')  # Remove empty strings
        click.echo(f"   Unique genres: {len(all_genres)}")
    
    if detailed:
        click.echo(f"\n📋 Column Information:")
        for col in df.columns:
            non_null = df[col].notna().sum()
            click.echo(f"   {col}: {non_null:,} non-null values")
        
        if 'Adult' in df.columns:
            adult_count = df['Adult'].sum() if 'Adult' in df.columns else 0
            click.echo(f"   Adult content: {adult_count:,} movies")


if __name__ == '__main__':
    cli()