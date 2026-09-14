import requests

BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT=10

def _get(endpoint):
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    return response.json()

def get_pokemon(name):
    return _get(f"pokemon/{name}")

def get_ability(name):
    return _get(f"ability/{name}")

def get_move(name):
    return _get(f"move/{name}")

def get_pokemon_summary(name):
    data = get_pokemon(name)

    return {
        "name": data["name"].capitalize(),
        "id":data["id"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [
            item["type"]["name"]
            for item in data["types"]
        ],
        "abilities": [
            item["ability"]["name"]
            for item in data["abilities"]
        ],
        "moves": [
            item["move"]["name"]
            for item in data["moves"]
        ],
    }