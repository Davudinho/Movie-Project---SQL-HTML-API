# omdb_api.py
import requests
import os

API_KEY = os.getenv("OMDB_API_KEY")

BASE_URL = "http://www.omdbapi.com/"


def fetch_movie(title):
    """Fetch movie data from OMDb API by title."""
    params = {
        "apikey": API_KEY,
        "t": title
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("Response") == "False":
            return None  # Movie not found

        return {
            "title": data.get("Title"),
            "year": int(data.get("Year")),
            "rating": float(data.get("imdbRating")),
            "poster": data.get("Poster")
        }

    except Exception:
        return "API_ERROR"
