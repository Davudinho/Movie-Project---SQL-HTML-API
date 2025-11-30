import json

data = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }

with open('data.json', 'w', encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)
    print(
        "JSON file created successfully."
    )
