from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import pandas as pd
import random
import os

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

def get_last_scraped_page(csv_path):
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path, usecols=["page"])
            if not df.empty:
                return df["page"].max()
        except Exception as e:
            print(f"Could not read CSV ({e}), starting fresh...")
    return 0 
csv_path = "data/anime_planet_full_details.csv"
last_page = get_last_scraped_page(csv_path)
start_page = last_page+1 if last_page else 1
max_pages = 751  



print(f"Resuming from page {start_page}...")
driver.get(f"https://www.anime-planet.com/anime/all?page={start_page}")
time.sleep(3)
actions = ActionChains(driver)


current_page = start_page
# while current_page < start_page:
#     try:
#         next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
#         driver.execute_script("arguments[0].click();", next_btn)
#         current_page += 1
#         time.sleep(3)
#     except:
#         print("Couldn't skip further, page not found.")
#         break

anime_data = []


while current_page <= max_pages:
    print(f"Scraping page {current_page}...")

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
                source = tooltip.find_element(By.CSS_SELECTOR,"div.tooltip.notes p").text[8:]
            except:
                source = None

            try:
                description = tooltip.find_element(By.CSS_SELECTOR, "p").text
            except:
                description = None
            
            anime_data.append({
                "title": title,
                "alt_title": alt_title,
                "type": type_text,
                "year": year,
                "rating": rating,
                "genres": genres,
                "source": source,
                "description": description,
                "img_url": img_url,
                "page":current_page
            })

            time.sleep(random.uniform(1, 2))

        except:
            pass

    if anime_data:
        df = pd.DataFrame(anime_data)
        df.to_csv(f"data/anime_planet_full_details.csv",mode='a',header=not os.path.exists("data/anime_planet_full_details.csv"), index=False, encoding="utf-8-sig")
        print(f"Appended {len(anime_data)} rows from page {current_page}.")
        anime_data = []

    print("Waiting before next page...")
    time.sleep(random.uniform(5, 8))
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
        driver.execute_script("arguments[0].click();", next_btn)
        current_page += 1
    except:
        print("No more pages.")
        break

# if anime_data:
#     df = pd.DataFrame(anime_data)
#     df.to_csv(f"data/anime_planet_page.csv",mode='a',header=not os.path.exists("data/anime_planet_full_details.csv"), index=False, encoding="utf-8-sig")

print("Scraping complete!")
driver.quit()
