# movie_storage_sql
import os
import requests
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FOLDER = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DB_FOLDER, "movies.db")


os.makedirs(DB_FOLDER, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def create_table():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                title TEXT PRIMARY KEY,
                year TEXT,
                rating TEXT,
                poster TEXT
            );
        """))


create_table()


def list_movies():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster FROM movies")
        )
        rows = result.fetchall()

        return {
            row[0]: {
                "year": row[1],
                "rating": row[2],
                "poster": row[3]
            }
            for row in rows
        }


def add_movie(title, year, rating, poster):
    with engine.connect() as connection:
        connection.execute(
            text("""
                INSERT INTO movies (title, year, rating, poster)
                VALUES (:title, :year, :rating, :poster)
            """),
            {"title": title, "year": year, "rating": rating, "poster": poster}
        )


def delete_movie(title: str) -> bool:
    if not isinstance(title, str):
        raise TypeError("title must be a string")

    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        return result.rowcount > 0


def update_movie(title: str, new_rating: int | float) -> bool:
    if not isinstance(title, str):
        raise TypeError("title must be a string")

    if not isinstance(new_rating, (int, float)):
        raise TypeError("new_rating must be a number")

    if not (0 <= new_rating <= 10):
        raise ValueError("new_rating must be between 0 and 10")

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                UPDATE movies SET rating = :rating
                WHERE title = :title
            """),
            {"rating": new_rating, "title": title}
        )
        return result.rowcount > 0


def get_movie_poster(title):
    """Fetch poster URL from OMDb API."""
    if API_KEY is None:
        return "https://via.placeholder.com/300x450?text=No+API+Key"

    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("Response") == "False":
            return "https://via.placeholder.com/300x450?text=No+Image"

        return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/300x450?text=Error"
