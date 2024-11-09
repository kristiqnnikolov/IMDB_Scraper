This project is a web scraping tool that uses Selenium to extract data from IMDB’s Top 250 rated movies.
Extracted data as follows : rank, title, release year, duration, genres, rating, votes, director, cast, and poster URL.

The scraped data is stored in JSON format for easy use and further analysis.
The project is specifically set up to run with Google Chrome.

Setup is pretty straight forward:
Install Required Packages:
```bash
pip install -r requirements.txt
```

Run the Scraper:
```bash
python imdb_scraper.py
```

Each movie is stored in a JSON file with the following structure:
```json
{
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
```
