import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.headless = True  # Run browser in headless mode (no UI)
chrome_options.add_argument("--disable-javascript")  # Disable JavaScript for faster loading

# Initialize Chrome WebDriver with specified options
driver = webdriver.Chrome(options=chrome_options)

# URL of IMDb Top 250 movies page
url = "https://www.imdb.com/chart/top/"
driver.get(url)  # Open the URL in headless browser

time.sleep(5)  # Allow time for page elements to load and prevent crashes

# Function to extract duration from a movie's details
def extract_duration():
    tags = driver.find_elements(By.CLASS_NAME, "ipc-inline-list__item")
    for tag in tags:
        tag_text = tag.text
        # Check if the text format matches "Xh Ymin" (e.g., "2h 30min")
        if len(tag_text) > 2 and tag_text[0].isdigit() and tag_text[1] == "h" and tag_text[2] == " ":
            return tag_text

# Function to extract release year (must be a 4-digit number)
def extract_year():
    tags = driver.find_elements(By.CLASS_NAME, "ipc-link.ipc-link--baseAlt.ipc-link--inherit-color")
    for tag in tags:
        tag_text = tag.text
        # Return if it is a 4-digit year
        if len(tag_text) == 4 and tag_text.isdigit():
            return tag_text

# Function to collect unique IMDb movie links from a list of elements
def get_hrefs(list_of_hrefs):
    for a_element in list_of_hrefs:
        href = a_element.get_attribute("href")
        # Add the href to the set only if it contains 'imdb' and limit the set to 250 items
        if "imdb" in href:
            href_set.add(href)
            if len(href_set) > 250:
                return

# Helper function to convert a list of Selenium elements to a list of text values
def extract_to_list(selenium_list):
    return [tags.text for tags in selenium_list]

# Initialize a set to store unique hrefs and a list to collect movie data
href_set = set()  # To hold unique URLs for each movie
movies_data = []  # List to store data for each movie

# Locate and collect all movie links on the main IMDb Top 250 page
a_elements = driver.find_elements(By.CLASS_NAME, "ipc-lockup-overlay.ipc-focusable")
get_hrefs(a_elements)

# Iterate through each unique movie URL to extract its details
for url in href_set:
    driver.get(url)  # Navigate to each movie's individual page
    print(f"Visiting: {url}")  # Print the URL for logging/debugging
    
    # Extract movie details
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

    # Extract cast and genre information
    actors = driver.find_elements(By.CLASS_NAME, "sc-cd7dc4b7-1.kVdWAO")
    cast_list = extract_to_list(actors)
    genres = driver.find_elements(By.CLASS_NAME, "ipc-chip.ipc-chip--on-baseAlt")
    genres_list = extract_to_list(genres)

    # Store all extracted movie data in a dictionary and add it to the list
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
    movies_data.append(movie_data)  # Add the movie's data dictionary to the list
    print(f"Successfully scraped: {url}")  # Log success message

# Write the list of movies' data to a JSON file
with open("movies_data.json", "w", encoding="utf-8") as f:
    json.dump(movies_data, f, ensure_ascii=False, indent=4)  # Write data with UTF-8 encoding
print('Sucessful scraping ! Ending script')
# Close the browser once done to free up resources
driver.quit()
