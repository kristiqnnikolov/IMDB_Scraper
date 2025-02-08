import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.headless = True  
chrome_options.add_argument("--disable-javascript")  

driver = webdriver.Chrome(options=chrome_options)

# URL of IMDb Top 250 movies page
url = "https://www.imdb.com/chart/top/"
driver.get(url)  

time.sleep(5)  

def extract_duration():
    tags = driver.find_elements(By.CLASS_NAME, "ipc-inline-list__item")
    for tag in tags:
        tag_text = tag.text
        if len(tag_text) > 2 and tag_text[0].isdigit() and tag_text[1] == "h" and tag_text[2] == " ":
            return tag_text

def extract_year():
    tags = driver.find_elements(By.CLASS_NAME, "ipc-link.ipc-link--baseAlt.ipc-link--inherit-color")
    for tag in tags:
        tag_text = tag.text
        if len(tag_text) == 4 and tag_text.isdigit():
            return tag_text

def get_hrefs(list_of_hrefs):
    for a_element in list_of_hrefs:
        href = a_element.get_attribute("href")
        if "imdb" in href:
            href_set.add(href)
            if len(href_set) > 250:
                return

def extract_to_list(selenium_list):
    return [tags.text for tags in selenium_list]

href_set = set()  
movies_data = [] 

a_elements = driver.find_elements(By.CLASS_NAME, "ipc-lockup-overlay.ipc-focusable")
get_hrefs(a_elements)

for url in href_set:
    driver.get(url)  
    print(f"Visiting: {url}")  
    
    rank = url.split('_')[-1]
    movie_title = driver.find_element(By.CLASS_NAME, "hero__primary-text").text
    year = extract_year()
    rating = driver.find_element(By.CLASS_NAME, "sc-d541859f-1.imUuxf").text
    votes = driver.find_element(By.CLASS_NAME, "sc-d541859f-3.dwhNqC").text
    duration = extract_duration()
    poster_url = driver.find_element(By.CLASS_NAME, "ipc-lockup-overlay.ipc-focusable").get_attribute("href")
    director = driver.find_element(
        By.CLASS_NAME,
        "ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link",
    ).text

    actors = driver.find_elements(By.CLASS_NAME, "sc-cd7dc4b7-1.kVdWAO")
    cast_list = extract_to_list(actors)
    genres = driver.find_elements(By.CLASS_NAME, "ipc-chip.ipc-chip--on-baseAlt")
    genres_list = extract_to_list(genres)

    movie_data = {
        "rank": rank,
        "title": movie_title,
        "year": year,
        "duration": duration,
        "genres": genres_list,
        "rating": rating,
        "votes": votes,
        "director": director,
        "cast": cast_list,
        "poster_url": poster_url
    }
    movies_data.append(movie_data)  
    print(f"Successfully scraped: {url}")  

with open("movies_data.json", "w", encoding="utf-8") as f:
    json.dump(movies_data, f, ensure_ascii=False, indent=4)  
print('Sucessful scraping ! Ending script')

driver.quit()
