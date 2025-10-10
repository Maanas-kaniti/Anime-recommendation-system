from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
import random
import os

# --- Stealth Setup ---
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# --- File Setup ---
csv_path = "data/anime_planet_full_details.csv"

# Load existing titles
existing_titles = set()
if os.path.exists(csv_path):
    try:
        df_existing = pd.read_csv(csv_path, usecols=["title"])
        existing_titles = set(df_existing["title"].dropna().astype(str))
        print(f"Loaded {len(existing_titles)} existing titles.")
    except Exception as e:
        print(f"Could not load existing titles: {e}")

# --- Append helper ---
def append_to_csv(row_dict):
    df = pd.DataFrame([row_dict])
    df.to_csv(csv_path,
              mode="a",
              header=not os.path.exists(csv_path),
              index=False,
              encoding="utf-8-sig")

# --- Pages you want to rescrape ---
pages_to_scrape = [2, 3, 4, 5, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 164, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 404, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 694, 730, 731]   # 🔥 Replace with your list

actions = ActionChains(driver)

for page_no in pages_to_scrape:
    print(f"\n🔄 Scraping page {page_no}...")
    driver.get(f"https://www.anime-planet.com/anime/all?page={page_no}")
    time.sleep(5)

    anime_cards = driver.find_elements(By.CSS_SELECTOR, ".crop")

    for card in anime_cards:
        img = card.find_element(By.TAG_NAME, "img")
        img_url = img.get_attribute("src")
        title_from_img = img.get_attribute("alt")

        actions.move_to_element(img).perform()

        try:
            tooltip = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ui-tooltip"))
            )

            try:
                title = tooltip.find_element(By.CSS_SELECTOR, "h5").text
            except:
                title = title_from_img

            # ✅ Skip if duplicate
            if title in existing_titles:
                print(f"Skipping duplicate: {title}")
                continue  

            try:
                alt_title = tooltip.find_element(By.CSS_SELECTOR, "h6").text[11:]
            except:
                alt_title = None

            try:
                type_text = tooltip.find_element(By.CSS_SELECTOR, ".type").text
            except:
                type_text = None

            try:
                year = tooltip.find_element(By.CSS_SELECTOR, ".iconYear").text
            except:
                year = None

            try:
                rating = tooltip.find_element(By.CSS_SELECTOR, ".ttRating").text
            except:
                rating = None

            try:
                genres = [g.text for g in tooltip.find_elements(By.CSS_SELECTOR, "div.tags ul li")]
            except:
                genres = []

            try:
                source = tooltip.find_element(By.CSS_SELECTOR, "div.tooltip.notes p").text[8:]
            except:
                source = None

            try:
                description = tooltip.find_element(By.CSS_SELECTOR, "p").text
            except:
                description = None

            # Build row
            row = {
                "title": title,
                "alt_title": alt_title,
                "type": type_text,
                "year": year,
                "rating": rating,
                "genres": genres,
                "source": source,
                "description": description,
                "img_url": img_url,
                "page": page_no
            }

            # Append immediately
            append_to_csv(row)
            existing_titles.add(title)

            print(f"✅ Appended: {title}")
            time.sleep(random.uniform(1, 2))

        except:
            print("⚠️ Tooltip fetch failed, skipping one anime.")

    print(f"✅ Finished page {page_no}")
    time.sleep(random.uniform(5, 8))

print("\n🎉 Selected page scraping complete!")
driver.quit()
