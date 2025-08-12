# Movie Dataset Analysis

This folder contains Jupyter notebooks for exploring and analyzing the TMDb movie dataset. Discover insights about movie trends, genre popularity, rating patterns, and industry dynamics through interactive visualizations and statistical analysis.

## Table of Contents

- [📊 Available Notebooks](#available-notebooks)
- [🚀 Quick Setup](#quick-setup)
- [🛠️ Dependencies](#dependencies)
- [📈 Key Insights Preview](#key-insights-preview)
- [🔍 Usage Tips](#usage-tips)
- [📁 File Structure](#file-structure)
- [🎯 Next Steps](#next-steps)
- [📚 Resources](#resources)

## Available Notebooks

### [`exploratory_analysis.ipynb`](./exploratory_analysis.ipynb)

**Complete dataset overview and fundamental insights**

- Dataset structure and data quality assessment
- Rating distribution analysis and statistics
- Genre frequency and popularity rankings
- Missing data patterns and data cleaning insights
- Top-rated movies and statistical summaries

### [`movie_trends.ipynb`](./movie_trends.ipynb)

**Temporal patterns and industry trend analysis**

- Genre popularity evolution across decades
- Rating trends over time periods
- Movie release patterns by year
- Industry growth and pattern analysis
- Correlation studies between different metrics

## Quick Setup

### Prerequisites

- Python 3.8+
- The main TMDb dataset ([`../tmdb_movies.csv`](../tmdb_movies.csv))

### Installation

From the project root directory:

1. **Install analysis dependencies:**

   ```bash
   pip install -r analysis/requirements-analysis.txt
   ```

2. **Launch Jupyter:**

   ```bash
   jupyter notebook analysis/
   ```

3. **Start exploring:**
   - Open `exploratory_analysis.ipynb` for dataset overview
   - Open `movie_trends.ipynb` for trend analysis

## Dependencies

The analysis notebooks require these packages (included in `requirements-analysis.txt`):

- **notebook** - Jupyter notebook server
- **pandas** - Data manipulation and analysis
- **matplotlib** - Basic plotting and visualizations
- **seaborn** - Statistical data visualization
- **plotly** - Interactive charts and plots
- **jupyter** - Notebook environment
- **numpy** - Numerical computing
- **ipykernel** - Python kernel for Jupyter
- **statsmodels** - Statistical modeling and hypothesis testing
- **ipython** - Enhanced interactive Python shell
- **kaleido** - Static image export for Plotly figures

## Key Insights Preview

**Discover answers to questions like:**

- Which movie genres are most popular over time?
- How have movie ratings changed across decades?
- What's the distribution of movie ratings in the dataset?
- Are there seasonal patterns in movie releases?
- Which years had the highest-rated movies?

## Usage Tips

**For best results:**

- Run cells sequentially in each notebook
- Interactive plots work best in Jupyter (not GitHub preview)
- Notebooks are designed to work with the 10,000-movie dataset
- Modify visualizations and analysis as needed for your use case

## File Structure

```
analysis/
├── README.md                    # This file
├── exploratory_analysis.ipynb   # Dataset overview and basic stats
└── movie_trends.ipynb          # Temporal analysis and trends
```

## Next Steps

**Extend the analysis:**

- Create custom visualizations for specific insights
- Build predictive models using the rating data
- Analyze genre combinations and patterns
- Export insights for reports or presentations

## Resources

- **Main Dataset**: [tmdb_movies.csv](../tmdb_movies.csv)
- **TMDb API Documentation**: [developers.themoviedb.org](https://developers.themoviedb.org)
- **Project Repository**: [github.com/HERALDEXX/tmdb-movie-scraper](https://github.com/HERALDEXX/tmdb-movie-scraper)

---

**Happy analyzing!** 🎬📊

_For questions or issues with the analysis notebooks, please open an issue in the main repository._

---

<div align="center">
    <p>
        <a href="https://raw.githubusercontent.com/HERALDEXX/tmdb-movie-scraper/refs/heads/main/LICENSE" target="_blank">
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="Click to View MIT License" style="vertical-align: middle;" />
        </a> <strong style="font-weight: bold;">• © 2025 Herald Inyang •</strong> 
        <a href="https://github.com/HERALDEXX" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-HERALDEXX-000?style=flat-square&logo=github" alt="GitHub Badge" style="vertical-align: middle;" />
        </a>
    </p>
</div>

---
