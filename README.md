# TMDb Movie Scraper (CLI Edition)

Powerful command-line tool that pulls up to **10,000** movie records from The Movie Database (TMDb) API with multiple output formats and advanced features.

**Supported Formats:** CSV | JSON | XLSX | SQLite

This repo contains an optimized Python scraper with a comprehensive Command-Line interface that uses TMDb's API to fetch movies and provides flexible data export options for portfolio and analysis work.

## Table of Contents

- [Features](#features)
- [Dataset](#dataset)
- [Setup](#setup)
  - [Getting Your TMDb API Key](#getting-your-tmdb-api-key)
- [CLI Usage](#cli-usage)
  - [**Alternative:** Package Installation](#alternative-package-installation)
  - [Basic Scraping](#basic-scraping)
  - [Advanced Options](#advanced-options)
  - [Data Management](#data-management)
- [Output Formats](#output-formats)
- [Legacy Usage](#legacy-usage)
- [Attribution](#attribution)
- [To-Do](#to-do)
- [License](#license)

## Features

### 🚀 **Performance Optimized**

- **Async/await** concurrent requests for maximum speed
- **Connection pooling** and intelligent rate limiting
- **Progress tracking** with real-time statistics
- Up to **10x faster** than traditional scrapers

### 🎛️ **Powerful CLI Interface**

- **Multiple output formats**: CSV, JSON, XLSX, SQLite
- **Configurable options**: movie count, concurrent requests, adult content
- **Data conversion** between formats
- **Dataset analysis** with summary statistics
- **Verbose/quiet modes** for different use cases

### 📊 **Smart Data Handling**

- **Auto-retry logic** with exponential backoff
- **Error handling** and logging
- **Data validation** and cleanup
- **Resume functionality** for interrupted scrapes

---

## Dataset

### TMDb Movies Dataset

- **Source**: The Movie Database (TMDb) API
- **Size**: ~10,000 movies (configurable)
- **Formats**: CSV, JSON, XLSX, SQLite
- **Default File**: [**`tmdb_movies.csv`**](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/feature/cli/tmdb_movies.csv)
- **JSON Convert**: [**`tmdb_movies.json`**](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/feature/cli/converts/tmdb_movies.json)
- **SQLite Convert**: [**`tmdb_movies.sqlite`**](https://github.com/HERALDEXX/tmdb-movie-scraper/blob/feature/cli/converts/tmdb_movies.sqlite)
- **XLSX (Excel) Convert**: [**`tmdb_movies.xlsx`**](https://github.com/HERALDEXX/tmdb-movie-scraper/blob/feature/cli/converts/tmdb_movies.xlsx)
- **Last Updated**: August 14, 2025
- **Selection Criteria**: Top movies sorted by popularity
- **Columns**: Title, Year, Rating, Description, Genre (plus `Adult` if enabled)

---

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/HERALDEXX/tmdb-movie-scraper.git
   ```

   ```bash
   cd tmdb-movie-scraper
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create your `.env` file:

   ```bash
   cp .env.example .env
   ```

   ### Getting Your TMDb API Key

   > You need a TMDb API key to run the scraper. Follow these steps to get your API key:

4. Get your TMDb API key (step-by-step)

   - Go to [https://www.themoviedb.org/](https://www.themoviedb.org/) and sign up / log in.

   - Click your profile avatar → **Settings**.

   - Choose **API** from the left menu.

   - Apply for an API key:

     **Application name:** e.g. `My TMDb Movie Scraper` or `My Movie Data Collector`

     **Application website / domain:** your GitHub URL (e.g., `https://github.com/yourusername`) or `http://localhost`

     **Application summary:** `Personal project to collect and analyze movie data from TMDb API for portfolio use.`

     For intended use, select **Personal / Portfolio / Learning** (or similar).

   - After submission you'll be shown an API key (a long string). **Do not share it publicly.**

5. Copy your TMDb API key and replace `your_api_key_here` in the `.env` file with your actual API key.

6. (Optional) Enable adult content in your `.env` file:

   ```env
   TMDB_INCLUDE_ADULT=true
   ```

---

> ⚠️ **Important:** Do not commit your `.env` file or API key to any **public** repo.

---

## CLI Usage

The scraper can be run directly using the `python cli_scraper.py` command. If you prefer, you can also install the package via `pip` (see below) to use a cleaner command name.

#### Alternative: Package Installation

If you prefer to install the project as a global command on your system, you can use the `setup.py` file:

```bash
pip install .
```

After installation, you can run the scraper from any directory using the `tmdb-scraper` command instead of `python cli_scraper.py`.

### Basic Scraping

Examples:

- Quick start - scrape 1,000 movies to CSV

```bash
python cli_scraper.py scrape
```

- Scrape 5,000 movies to JSON format

```bash
python cli_scraper.py scrape --count 5000 --format json --output movies.json
```

- High-speed scraping with 12 concurrent requests

```bash
python cli_scraper.py scrape -c 10000 --concurrent 12 --verbose
```

### Advanced Options

Examples:

- Include adult content and save to SQLite

```bash
python cli_scraper.py scrape --count 5000 --include-adult --format sqlite --output movies.sqlite3
```

**or**

```bash
python cli_scraper.py scrape --count 5000 --include-adult --format sqlite --output movies.sqlite
```

**or**

```bash
python cli_scraper.py scrape --count 5000 --include-adult --format sqlite --output movies.db
```

- Quiet mode for automated scripts

```bash
python cli_scraper.py scrape --count 2000 --quiet --output data/movies.xlsx
```

- Full configuration example

```bash
python cli_scraper.py scrape \
    --count 10000 \
    --output premium_movies.json \
    --format json \
    --concurrent 8 \
    --include-adult \
    --verbose
```

### Data Management

Examples:

- Analyze existing dataset

```bash
python cli_scraper.py info tmdb_movies.csv
```

- Convert between formats

```bash
python cli_scraper.py convert movies.csv movies.sqlite --to-format sqlite
```

```bash
python cli_scraper.py convert data.json data.xlsx --to-format xlsx
```

- Check configuration and test API

```bash
python cli_scraper.py config
```

# Get help for any command

```bash
python cli_scraper.py --help
```

```bash
python cli_scraper.py scrape --help
```

### CLI Command Reference

| Command   | Description                 | Example                                       |
| --------- | --------------------------- | --------------------------------------------- |
| `scrape`  | Scrape movies from TMDb API | `scrape --count 5000 --format json`           |
| `info`    | Show dataset information    | `info movies.csv`                             |
| `convert` | Convert between formats     | `convert data.csv data.json --to-format json` |
| `config`  | Check configuration         | `config`                                      |

### CLI Options

| Option            | Short | Description                          | Default         |
| ----------------- | ----- | ------------------------------------ | --------------- |
| `--count`         | `-c`  | Number of movies to scrape           | 1000            |
| `--output`        | `-o`  | Output filename                      | tmdb_movies.csv |
| `--format`        | `-f`  | Output format (csv/json/xlsx/sqlite) | csv             |
| `--concurrent`    |       | Concurrent requests                  | 8               |
| `--include-adult` |       | Include adult content                | False           |
| `--verbose`       | `-v`  | Enable verbose output                | False           |
| `--quiet`         | `-q`  | Suppress output                      | False           |

---

## Output Formats

### CSV Format

```csv
Title,Year,Rating,Description,Genre
The Shawshank Redemption,1994,9.3,"Two imprisoned men bond...",Drama
The Godfather,1972,9.2,"The aging patriarch...",Drama Crime
```

### JSON Format

```json
[
  {
    "Title": "The Shawshank Redemption",
    "Year": "1994",
    "Rating": 9.3,
    "Description": "Two imprisoned men bond...",
    "Genre": "Drama"
  }
]
```

### SQLite Database

- Table name: `movies`
- Columns: Title, Year, Rating, Description, Genre, Adult (if enabled)
- Indexed for fast queries

### XLSX (Excel)

- Clean formatting with headers
- Suitable for business presentations
- Compatible with Excel, Google Sheets, etc.

---

## Legacy Usage

> For backward compatibility, you can still use the original scraper:

```bash
python tmdb_scraper.py
```

This runs the optimized async scraper with default settings (10,000 movies to CSV).

---

## Attribution

Data provided by TMDb ([https://www.themoviedb.org](https://www.themoviedb.org))

---

## To-Do

### Completed ✅

- [x] **Async optimization** - 10x performance improvement
- [x] **CLI interface** - Command-line tool with multiple options
- [x] **Multiple formats** - JSON, XLSX, SQLite support
- [x] **Data conversion** - Convert between formats
- [x] **Progress tracking** - Real-time progress bars
- [x] **Configuration management** - Easy setup and validation

### Planned 🔄

- [ ] **Web dashboard** - Browser-based interface
- [ ] **Advanced filtering** - Genre, year, rating filters
- [ ] **Data analysis** - Built-in statistics and insights
- [ ] **API read access token** - Enhanced authentication
- [ ] **Pagination beyond 10K** - Fetch unlimited movies
- [ ] **Export templates** - Custom output formats
- [ ] **Scheduled scraping** - Automated data updates

---

## License

This project is licensed under the [`MIT License`](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/main/LICENSE)

---

<div align="center">
    <p>
        <a href="https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/main/LICENSE" target="_blank">
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="Click to View MIT License" style="vertical-align: middle;" />
        </a>
        <strong style="font-weight: bold;"> • © 2025 Herald Inyang • </strong> 
        <a href="https://github.com/HERALDEXX" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-HERALDEXX-000?style=flat-square&logo=github" alt="GitHub Badge" style="vertical-align: middle;" />
        </a>
    </p>
</div>

---
