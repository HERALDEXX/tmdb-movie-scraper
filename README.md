# TMDb Movie Scraper

Simple script that pulls **10,000** movie records from The Movie Database (TMDb) API and writes a CSV with these columns:

**Title | Year | Rating | Description | Genre**

This repo contains a minimal Python scraper that uses TMDb's API (discover endpoint) to fetch movies page-by-page and saves a CSV suitable for portfolio work.

## Table of Contents

- [Dataset](#dataset)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Output CSV](#output-csv)
- [Attribution](#attribution)
- [To-Do](#to-do)
- [License](#license)

## Dataset

### TMDb Movies Dataset
- **Source**: The Movie Database (TMDb) API
- **Size**: 10,000 movies
- **Format**: CSV
- **File**: [**`tmdb_movies.csv`**](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/refs/heads/main/tmdb_movies.csv)
- **Last Updated**: August 11, 2025
- **Selection Criteria**: Top movies sorted by popularity
- **Columns**: Title, Year, Rating, Description, Genre

---

## Getting Started

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

5. Get your TMDb API key (step-by-step)

   - Go to [https://www.themoviedb.org/](https://www.themoviedb.org/) and sign up / log in.

   - Click your profile avatar → **Settings**.

   - Choose **API** from the left menu.

   - Apply for an API key:

     **Application name:** e.g. `My TMDb Movie Scraper` or `My Movie Data Collector`

     **Application website / domain:** your GitHub URL (e.g., `https://github.com/yourusername`) or `http://localhost`

     **Application summary:** `Personal project to collect and analyze movie data from TMDb API for portfolio use.`

     For intended use, select **Personal / Portfolio / Learning** (or similar).

   - After submission you’ll be shown an API key (a long string). **Do not share it publicly.**

6. Copy your TMDb API key and replace `your_api_key_here` in the `.env` file, with your actual API key.

---

> Do not commit your `.env` file or API key to a public repo.

---

## Usage

1. Make sure your `.env` contains `TMDB_API_KEY` (or export the variable in your shell).
2. Run the scraper:

   ```bash
   python tmdb_scraper.py
   ```

The script writes and/or updates `tmdb_movies.csv` in the project folder.

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
- Store scraped data in a better format, instead of CSV e.g. 
   - [ ] Use JSON,
   - [ ] Use SQLite,
   - [ ] Use XLSX,
   - [ ] Use XML,
   - [ ] Use PostgreSQL / MySQL,
   **or**
   - [ ] Other
- [ ] Use API read access token instead of API key.
- [ ] Pagination to fetch more than 10,000 movies.

---

## License

This project is licensed under the [`MIT License`](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/refs/heads/main/LICENSE)

---

<div align="center">
    <p>
        <strong style="font-weight: bold;">MIT Licensed • © 2025 Herald Inyang •</strong> 
        <a href="https://github.com/HERALDEXX" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-HERALDEXX-000?style=flat-square&logo=github" alt="GitHub Badge" style="vertical-align: middle;" />
        </a>
    </p>
    <p>
        <a href="https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/refs/heads/main/LICENSE" target="_blank">
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="Click to View MIT License" style="vertical-align: middle;" />
        </a>
    </p>
</div>

---
