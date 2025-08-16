# TMDb Movie Scraper (Web Dashboard)

Optimized script that pulls up to **10,000** movie records from The Movie Database (TMDb) API with a modern web interface for easy configuration and real-time monitoring.

**Title | Year | Rating | Description | Genre**

This repo contains the optimized Python scraper from the api-optimization branch plus a new web dashboard that provides a user-friendly interface for configuring scraping parameters and monitoring progress.

## Table of Contents

- [Dataset](#dataset)
- [Web Dashboard](#web-dashboard)
- [Setup](#setup)
  - [Getting Your TMDb API Key](#getting-your-tmdb-api-key)
- [Usage](#usage)
  - [Web Interface (Recommended)](#web-interface-recommended)
  - [Direct Script (Alternative)](#direct-script-alternative)
- [Output Formats](#output-formats)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Attribution](#attribution)
- [To-Do](#to-do)
- [License](#license)

## Dataset

### TMDb Movies Dataset

- **Source**: The Movie Database (TMDb) API
- **Size**: ~10,000 movies
- **Format**: CSV
- **File**: Generated with timestamp (e.g., [`tmdb_movies_20250816_132926_186c814f.csv`](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/feature/web-dashboard/tmdb_movies_20250816_132926_186c814f.csv))
- **Selection Criteria**: Top movies sorted by popularity
- **Columns**: Title, Year, Rating, Description, Genre (plus `Adult` if `TMDB_INCLUDE_ADULT` is enabled)

---

## Web Dashboard

**New Feature**: Modern web interface with real-time progress tracking, multiple export formats, and intuitive configuration.

### Features
- 🎨 **Modern UI**: Clean, responsive design that works on all devices
- 📊 **Live Progress**: Real-time scraping progress with visual indicators
- ⚙️ **Easy Configuration**: Web-based parameter adjustment (movies count, concurrent requests, adult content)
- 📝 **Activity Logging**: Color-coded real-time logs
- 🔧 **API Validation**: Automatic API key verification
- 📁 **CSV Export**: Download results as CSV files

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

3. Switch to the web dashboard branch:

   ```bash
   git checkout feature/web-dashboard
   ```

4. Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Create your `.env` file:

   ```bash
   cp .env.example .env
   ```

   ### Getting Your TMDb API Key

   > You need a TMDb API key to run the scraper. Follow these steps:

6. Get your TMDb API key (step-by-step)

   - Go to [https://www.themoviedb.org/](https://www.themoviedb.org/) and sign up / log in.

   - Click your profile avatar → **Settings**.

   - Choose **API** from the left menu.

   - Apply for an API key:

     **Application name:** e.g. `My TMDb Movie Scraper` or `My Movie Data Collector`

     **Application website / domain:** your GitHub URL (e.g., `https://github.com/yourusername`) or `http://localhost`

     **Application summary:** `Personal project to collect and analyze movie data from TMDb API for portfolio use.`

     For intended use, select **Personal / Portfolio / Learning** (or similar).

   - After submission you'll be shown an API key (a long string). **Do not share it publicly.**

7. Copy your TMDb API key and replace `your_api_key_here` in the `.env` file, with your actual API key.

8. Toggle `TMDB_INCLUDE_ADULT` in your `.env` file to `true` if you want to include adult content in the dataset.

   ```env
   TMDB_INCLUDE_ADULT=true
   ```
> **Important**: Do not commit your `.env` file or API key to a public repo.

---

## Usage

### Web Interface (Recommended)

1. Start the web dashboard:

   ```bash
   python app.py
   ```

2. Open your browser to: **[http://localhost:8000](http://localhost:8000)**

3. Configure your scraping parameters:
   - **Number of movies**: 1-10,000
   - **Concurrent requests**: 1-20 (8 recommended)
   - **Adult content**: Toggle on/off
   - **Output format**: CSV (currently only format supported)

4. Click **"Start Scraping"** and monitor real-time progress

5. Download your file when complete

6. Press **`Ctrl`** + **`C`** in your terminal, to stop the server.

### Direct Script (Alternative)

You can still run the optimized scraper directly:

```bash
python tmdb_scraper.py
```

> The script writes and/or updates `tmdb_movies.csv` with latest data from TMDb API.

**Note**: Currently only CSV format is supported. Use the web interface for easier configuration and real-time progress monitoring.

---

## Output Format

### CSV (Both Methods)

Columns:

- `Title` — movie title
- `Year` — release year (YYYY)
- `Rating` — TMDb `vote_average`
- `Description` — overview (single line)
- `Genre` — comma-separated genre names
- `Adult` — `true` if movie is adult content (column only present if `TMDB_INCLUDE_ADULT` is enabled)

*Both the web interface and direct script output CSV format.*

---

## Configuration

### Environment Variables (.env)
```env
TMDB_API_KEY=your_api_key_here
TMDB_INCLUDE_ADULT=false  # Set to true to include adult content
```

### Web Dashboard Settings
- **Movies Count**: 1-10,000 (default: 1,000)
- **Concurrent Requests**: 1-20 (default: 8)
- **Output Format**: CSV/JSON/XLSX
- **Adult Content**: Include/exclude adult-rated movies

### Performance Tuning
- **8 concurrent requests**: Good for most connections
- **Higher concurrency**: Faster scraping but requires stable internet
- **Lower concurrency**: More reliable for slower connections

---

## File Structure

```
tmdb-movie-scraper/
├── tmdb_scraper.py           # Core scraping engine
├── app.py                    # Web dashboard server
├── requirements.txt          # Dependencies (includes web dashboard)
├── templates/
│   └── index.html           # Dashboard interface
├── .env                     # Your configuration
└── README.md                # This file
```

---

## Troubleshooting

### Common Issues

**API Key Missing:**
- Ensure `TMDB_API_KEY` is set in your `.env` file
- Verify your key at [TMDb Settings](https://www.themoviedb.org/settings/api)

**Web Dashboard Won't Start:**
- Check if port 8000 is available: `python app.py`
- Try a different port: `uvicorn app:app --port 8001`

**Slow Performance:**
- Reduce concurrent requests for slower internet
- Check your internet connection stability
- Monitor TMDb API rate limits

**Download Issues:**
- Ensure scraping completed successfully
- Check browser download permissions
- Try refreshing the page

---

## Attribution

Data provided by TMDb ([https://www.themoviedb.org](https://www.themoviedb.org))

---

## To-Do

- Store scraped data in a better format, instead of CSV e.g.
  - [ ] Use JSON
  - [ ] Use SQLite
  - [ ] Use XLSX
  - [ ] Use XML
  - [ ] Use PostgreSQL / MySQL
        **or**
  - [ ] Other
- [ ] Use API read access token instead of API key
- [ ] Pagination to fetch more than 10,000 movies
- [ ] Advanced filtering options in web dashboard
- [ ] Scheduled scraping
- [ ] Data visualization charts

---

## License

This project is licensed under the [`MIT License`](https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/main/LICENSE)

---

<div align="center">
    <p>
        <a href="https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/main/LICENSE" target="_blank">
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="Click to View MIT License" style="vertical-align: middle;" />
        </a><strong style="font-weight: bold;">• © 2025 Herald Inyang •</strong> 
        <a href="https://github.com/HERALDEXX" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-HERALDEXX-000?style=flat-square&logo=github" alt="GitHub Badge" style="vertical-align: middle;" />
        </a>
    </p>
</div>

---