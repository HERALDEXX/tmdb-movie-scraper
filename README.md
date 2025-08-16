# TMDb Movie Scraper

Simple script that pulls up to **10,000** movie records from The Movie Database (TMDb) API and writes a CSV with these columns:

**Title | Year | Rating | Description | Genre**

This repo contains a minimal Python scraper that uses TMDb's API (discover endpoint) to fetch movies page-by-page and saves a CSV suitable for portfolio work.

---

## Table of Contents

- [Dataset](#dataset)
- [Analysis](#analysis)
- [Setup](#setup)
  - [Getting Your TMDb API Key](#getting-your-tmdb-api-key)
- [Usage/Updating Dataset](#usageupdating-dataset)
   - [Basic Usage (This Branch)](#basic-usage-this-branch)
   - [**Web Dashboard (Recommended)**](#web-dashboard)
   - [CLI Edition](#cli-edition)
   - [API Optimization](#api-optimization)
- [Output CSV](#output-csv)
- [Attribution](#attribution)
- [To-Do](#to-do)
- [License](#license)

## Dataset

### TMDb Movies Dataset

- **Source**: The Movie Database (TMDb) API
- **Size**: ~10,000 movies
- **Format**: CSV
- **File**: [**`tmdb_movies.csv`**](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/main/tmdb_movies.csv)
- **Last Updated**: August 11, 2025
- **Selection Criteria**: Top movies sorted by popularity
- **Columns**: Title, Year, Rating, Description, Genre

---

## Analysis

Detailed data exploration live in the [**`feature/analysis-notebooks`**](https://github.com/HERALDEXX/tmdb-movie-scraper/tree/feature/analysis-notebooks) branch

See [analysis/README.md](https://github.com/HERALDEXX/tmdb-movie-scraper/blob/feature/analysis-notebooks/analysis/README.md) for more details.

---

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/HERALDEXX/tmdb-movie-scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd tmdb-movie-scraper
   ```

3. Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create your `.env` file:

   ```bash
   cp .env.example .env
   ```

   ### Getting Your TMDb API Key

   > You need a TMDb API key to run the scraper. Follow these remaining steps to get your API key:

5. Get your TMDb API key (step-by-step)

   - Go to [https://www.themoviedb.org/](https://www.themoviedb.org/) and sign up / log in.

   - Click your profile avatar → **Settings**.

   - Choose **API** from the left menu.

   - Apply for an API key:

     **Application name:** e.g. `My TMDb Movie Scraper` or `My Movie Data Collector`

     **Application website / domain:** your GitHub URL (e.g., `https://github.com/yourusername`) or `http://localhost`

     **Application summary:** `Personal project to collect and analyze movie data from TMDb API for portfolio use.`

     For intended use, select **Personal / Portfolio / Learning** (or similar).

   - After submission you'll be shown an API key (a long string). **Do not share it publicly.**

6. Copy your TMDb API key and replace `your_api_key_here` in the `.env` file, with your actual API key.

---

> Do not commit your `.env` file or API key to a public repo.

---

## Usage/Updating Dataset

### Basic Usage (This Branch)

> To update the dataset with latest data from TMDb using the basic scraper:

1. Make sure your `.env` contains `TMDB_API_KEY` (or export the variable in your shell).
2. Run the scraper:

   ```bash
   python tmdb_scraper.py
   ```

> The script writes and/or updates `tmdb_movies.csv` with latest data from TMDb API.

---

### Web Dashboard

Interactive browser-based dashboard **(with live scraping, abort controls, and dataset downloads)** is available in the [**`feature/web-dashboard`**](https://github.com/HERALDEXX/tmdb-movie-scraper/tree/feature/web-dashboard) branch.

---

### CLI Edition

Powerful command-line tool **(with multiple output formats & advanced features)** is available in the [**`feature/cli`**](https://github.com/HERALDEXX/tmdb-movie-scraper/tree/feature/cli) branch.

---

### API Optimization

Optimized scraper **(with improved speed & efficiency)** is available in the [**`feature/api-optimization`**](https://github.com/HERALDEXX/tmdb-movie-scraper/tree/feature/api-optimization) branch.

---

## Output CSV

Columns:

- `Title` — movie title
- `Year` — release year (YYYY)
- `Rating` — TMDb `vote_average`
- `Description` — overview (single line)
- `Genre` — comma-separated genre names

---

## Attribution

Data provided by TMDb ([https://www.themoviedb.org](https://www.themoviedb.org))

---

## To-Do

### Completed ✅

- [x] **API Optimization** - Async scraping with 10x performance improvement
- [x] **CLI Interface** - Command-line tool with multiple formats
- [x] **Multiple output formats** - JSON, XLSX, SQLite support
- [x] **Data conversion tools** - Convert between formats
- [x] **Analysis notebooks** - Data exploration and insights
- [x] **Web dashboard** - Browser-based interface

### In Progress 🔄

- [ ] **Advanced filtering** - Genre, year, rating filters

### Planned 📋

- [ ] **API read access token** - Enhanced authentication
- [ ] **Pagination beyond 10K** - Fetch unlimited movies
- [ ] **Scheduled scraping** - Automated data updates
- [ ] **PostgreSQL / MySQL** - Enterprise database support

---

## License

MIT License - see [LICENSE](./LICENSE) file for details.
---

<div align="center">
    <p>
        <strong>© 2025 Herald Inyang</strong> • 
        <a href="https://github.com/HERALDEXX" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-HERALDEXX-000?style=flat-square&logo=github" alt="GitHub Badge" style="vertical-align: middle;" />
        </a> • 
        <a href="https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/main/LICENSE" target="_blank">
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="MIT License" style="vertical-align: middle;" />
        </a>
    </p>
</div>

---
