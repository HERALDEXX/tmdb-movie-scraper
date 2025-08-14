#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tmdb-movie-scraper",
    version="1.0.0",
    author="Herald Inyang",
    author_email="inyangheraldmbre@outlook.com",
    description="A powerful CLI tool to scrape movie data from The Movie Database (TMDb)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HERALDEXX/tmdb-movie-scraper",
    py_modules=["cli_scraper", "tmdb_scraper"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tmdb-scraper=cli_scraper:cli",
        ],
    },
)
