import json

PATH = "C:/Users/User/PycharmProjects/Filmdatenbank_II/data.json"


def get_movies():
    try:
        with open(PATH, "r") as f:
            movies = json.load(f)
    except FileNotFoundError:
        movies = {}
    return movies


def save_movies(movies):
    with open(PATH, "w") as f:
        json.dump(movies, f, indent=4)


def add_movie(title, year, rating):
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)


def update_movie(title, rating):
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)
