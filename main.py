import requests
from app.sources.pokeapi import get_pokemon_summary

name = input("Enter pokemon name: ") or "pikachu"

try:
    pokemon = get_pokemon_summary(name)

    print(f"\nName: {pokemon['name']}")
    print(f"ID: {pokemon['id']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print(f"Types: {', '.join(pokemon['types'])}")
    print(f"Abilities: {', '.join(pokemon['abilities'])}")

    print("\nMoves:")
    for move in pokemon["moves"]:
        print(f" - {move}")

except requests.HTTPError as e:
    if e.response.status_code == 404:
        print(f"\nPokémon '{name}' was not found.")
    else:
        print(f"\nAPI error: {e}")

except requests.RequestException as e:
    print(f"\nNetwork error: {e}")