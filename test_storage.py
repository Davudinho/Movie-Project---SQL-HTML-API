# test_storage.py
from storage.movie_storage_sql import add_movie, list_movies, delete_movie, update_movie

print("\n--- ADD MOVIE ---")
add_movie("Inception", 2010, 8.8)

print("\n--- LIST MOVIES ---")
print(list_movies())

print("\n--- UPDATE MOVIE ---")
update_movie("Inception", 9.0)
print(list_movies())

print("\n--- DELETE MOVIE ---")
delete_movie("Inception")
print(list_movies())
