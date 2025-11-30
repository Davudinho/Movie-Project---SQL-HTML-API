# movies.py
import os
from storage import movie_storage_sql as storage
import random


def command_list_movies():
    """List all movies stored in the database."""
    movies = storage.list_movies()

    if not movies:
        print("No movies found.")
        return

    print(f"{len(movies)} movies in total:\n")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']} ⭐")


def command_add_movie():
    """Add a new movie to the database."""
    title = input("Enter movie title: ").strip()
    year = input("Enter release year: ").strip()
    rating = input("Enter rating (0–10): ").strip()

    poster = storage.get_movie_poster(title)  # OMDb API

    storage.add_movie(title, year, rating, poster)
    print(f"Movie '{title}' was added successfully.")


def command_delete_movie():
    """Delete a movie by title."""
    title = input("Enter movie title to delete: ").strip()

    if storage.delete_movie(title):
        print(f"Movie '{title}' was deleted.")
    else:
        print("Movie not found.")


def command_update_movie():
    """Update the rating of a movie."""
    title = input("Enter movie title to update: ").strip()
    new_rating = float(input("Enter new rating (0–10): "))

    if storage.update_movie(title, new_rating):
        print(f"Movie '{title}' was updated.")
    else:
        print("Movie not found.")


def command_stats():
    """Display basic statistics about the movie database."""
    movies = storage.list_movies()

    if not movies:
        print("No movies available.")
        return

    ratings = [float(data["rating"]) for data in movies.values()]

    avg = sum(ratings) / len(ratings)
    best = max(movies.items(), key=lambda x: float(x[1]["rating"]))
    worst = min(movies.items(), key=lambda x: float(x[1]["rating"]))

    print("\n=== Statistics ===")
    print(f"Average rating: {avg:.2f}")
    print(f"Best movie: {best[0]} ({best[1]['rating']})")
    print(f"Worst movie: {worst[0]} ({worst[1]['rating']})")


def command_random_movie():
    """Select and display a random movie."""
    movies = storage.list_movies()

    if not movies:
        print("No movies available.")
        return

    title = random.choice(list(movies.keys()))
    data = movies[title]

    print("\n=== Random Movie ===")
    print(f"{title} ({data['year']}): {data['rating']} ⭐")


def command_search_movie():
    """Search a movie by partial title."""
    query = input("Enter search term: ").lower().strip()
    movies = storage.list_movies()

    matches = {t: d for t, d in movies.items() if query in t.lower()}

    if matches:
        print(f"\nFound {len(matches)} match(es):")
        for title, data in matches.items():
            print(f"- {title} ({data['year']}) Rating: {data['rating']}")
    else:
        print("No matches found.")


def command_sorted_by_rating():
    """Display movies sorted by rating (highest first)."""
    movies = storage.list_movies()

    sorted_movies = sorted(
        movies.items(),
        key=lambda x: float(x[1]["rating"]),
        reverse=True
    )

    print("\n=== Movies Sorted by Rating ===")
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']} ⭐")


def command_generate_website():
    """Generate an HTML website using the template file."""

    template_path = "static/index_template.html"
    output_path = "index.html"

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print("Error: Template file not found.")
        print("Expected path:", os.path.abspath(template_path))
        return

    movies = storage.list_movies()

    movie_items = ""
    for title, data in movies.items():
        movie_items += f"""
        <div class="movie">
            <img src="{data['poster']}" alt="{title}" />
            <h2>{title}</h2>
            <p>Year: {data['year']}</p>
            <p>Rating: {data['rating']}</p>
        </div>
        """

    html_content = (
        template
        .replace("__TEMPLATE_TITLE__", "My Movie Collection")
        .replace("__TEMPLATE_MOVIE_GRID__", movie_items)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Website was generated successfully.")


def main():
    """Display menu and process user commands."""
    MENU = {
        "1": command_list_movies,
        "2": command_add_movie,
        "3": command_delete_movie,
        "4": command_update_movie,
        "5": command_stats,
        "6": command_random_movie,
        "7": command_search_movie,
        "8": command_sorted_by_rating,
        "9": command_generate_website,
    }

    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website")

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice in MENU:
            MENU[choice]()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
