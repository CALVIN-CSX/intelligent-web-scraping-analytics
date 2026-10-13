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

    pokemon_data = []
    pokemon_data.append({
        "name": data["name"].capitalize(),
        "id": data["id"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [item["type"]["name"] for item in data["types"]],
        "abilities": [item["ability"]["name"] for item in data["abilities"]],
        "moves": [item["move"]["name"] for item in data["moves"]],
    })

    return pokemon_data
def get_pokemon_summary_output(pokemon_name):
    try:
        pokemon = get_pokemon_summary(pokemon_name)
        print(f"\nName: {pokemon[0]['name']}")
        print(f"ID: {pokemon[0]['id']}")
        print(f"Height: {pokemon[0]['height']}")
        print(f"Weight: {pokemon[0]['weight']}")
        print(f"Types: {', '.join(pokemon[0]['types'])}")
        print(f"Abilities: {', '.join(pokemon[0]['abilities'])}")

        print("\nMoves:")
        for move in pokemon[0]["moves"]:
            print(f" - {move}")


    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print(f"\nPokémon '{pokemon_name}' was not found.")
        else:
            print(f"\nAPI error: {e}")

    except requests.RequestException as e:
        print(f"\nNetwork error: {e}")