# Anime Recommendation System Scraper

This project scrapes anime data from Anime-Planet and stores it in a CSV file for further analysis or recommendation system development.

## File Overview

### `scraper.py`

- **Purpose:** Main scraper script for Anime-Planet.
- **Functionality:**
  - Uses Selenium to automate browser actions and scrape anime details (title, alt title, type, year, rating, genres, source, description, image URL, page).
  - Resumes scraping from the last completed page by reading the `page` column in the CSV.
  - Appends new data to `data/anime_planet_full_details.csv`.
  - Handles stealth browser setup to avoid detection.
  - Scrapes all pages up to a specified maximum.

### `Back_up_scraper.py`

- **Purpose:** Backup/rescrape script for specific pages.
- **Functionality:**
  - Uses Selenium to scrape only selected pages (useful for fixing missing or corrupted data).
  - Checks for duplicate titles before appending to the CSV.
  - Appends only new/unique anime entries to `data/anime_planet_full_details.csv`.
  - Stealth browser setup similar to the main scraper.

### `requirements.txt`

- **Purpose:** Lists Python dependencies for the project.
- **Contents:**
  - `selenium` (browser automation)
  - `webdriver-manager` (manages browser drivers)
  - `pandas` (data manipulation)
  - `beautifulsoup4` (HTML parsing, not currently used in main scripts)
  - `scikit-learn` (machine learning, not currently used in main scripts)
  - `tqdm` (progress bars, not currently used in main scripts)

### `data/anime_planet_full_details.csv`

- **Purpose:** Stores all scraped anime data.
- **Contents:**
  - Columns: `title`, `alt_title`, `type`, `year`, `rating`, `genres`, `source`, `description`, `img_url`, `page`
  - Each row contains details for one anime entry scraped from Anime-Planet.

## Usage

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the main scraper:**

   ```sh
   python scraper.py
   ```

   - Scrapes all anime pages, resumes from last page if interrupted.

3. **Run the backup/rescrape script:**
   ```sh
   python Back_up_scraper.py
   ```
   - Scrapes only specified pages, skips duplicates.

## Notes

- Both scripts require Chrome and ChromeDriver.
- Output is saved to `data/anime_planet_full_details.csv`.
- For large scrapes, ensure a stable internet connection and sufficient disk space.

## Folder Structure

- `scraper.py` – Main scraper script.
- `Back_up_scraper.py` – Backup/specific page scraper.
- `requirements.txt` – Python dependencies.
- `data/anime_planet_full_details.csv` – Output data file.

---

Feel free to modify the scripts or add new features for your
