# Anime Recommendation System

This project scrapes anime data from Anime-Planet, cleans and processes it, and provides a content-based recommendation system using genres and descriptions.

## Project Structure & File Overview

```
Anime-recommendation-system/
│
├── scraper.py
├── Back_up_scraper.py
├── requirements.txt
├── Readme.md
│
├── data/
│   ├── anime_planet_full_details.csv
│   ├── anime_planet_full_details_.csv
│   └── anime_planet_full_details_cleaned.csv
│
├── anime_recommender.ipynb
└── clean-data.ipynb
```

### `scraper.py`

- **Purpose:** Main web scraper for Anime-Planet.
- **Details:** Uses Selenium to collect anime details (title, alt_title, type, year, rating, genres, source, description, img_url, page) and saves them to `data/anime_planet_full_details.csv`.

### `Back_up_scraper.py`

- **Purpose:** Backup/specific page scraper.
- **Details:** Scrapes selected pages, checks for duplicates, and appends unique entries to the main CSV.

### `requirements.txt`

- **Purpose:** Lists all Python dependencies.
- **Contents:** selenium, webdriver-manager, pandas, beautifulsoup4, scikit-learn, tqdm.

### `data/anime_planet_full_details.csv`

- **Purpose:** Raw scraped anime data.
- **Columns:** `title`, `alt_title`, `type`, `year`, `rating`, `genres`, `source`, `description`, `img_url`, `page`.

### `data/anime_planet_full_details_.csv`

- **Purpose:** Intermediate cleaned data file.
- **Details:** Contains additional columns like `type_only` and `episodes` extracted from the raw data.

### `data/anime_planet_full_details_cleaned.csv`

- **Purpose:** Final cleaned dataset for analysis and recommendations.
- **Details:** Missing values handled, genres formatted, episode numbers cleaned.

### `clean-data.ipynb`

- **Purpose:** Data cleaning and preprocessing notebook.
- **Details:** Loads raw data, extracts and cleans columns, handles missing values, and saves cleaned data for use in recommendations.

### `anime_recommender.ipynb`

- **Purpose:** Main notebook for building and running the recommendation system.
- **Details:**
  - Loads cleaned data.
  - Processes genres and descriptions.
  - Vectorizes features using CountVectorizer (genres) and TfidfVectorizer (descriptions).
  - Computes similarity matrices.
  - Provides functions to recommend anime by genre or description similarity.

## Usage

1. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Scrape data:**

   ```sh
   python scraper.py
   ```

3. **Clean data:**

   - Run `clean-data.ipynb` in Jupyter to process and clean the raw CSV.

4. **Run recommendations:**
   - Open `anime_recommender.ipynb` and use the provided functions to get anime recommendations by genre or description.

## Notes

- All data files are stored in the `data/` directory.
- The recommendation system uses content-based filtering (genres and descriptions).
- You can extend the notebooks to use other features (ratings, year, etc.) for more advanced recommendations.

---

Feel free to explore, modify, and build upon this project for your anime recommendation needs!
