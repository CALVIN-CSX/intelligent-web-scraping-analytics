def normalize_wikipedia(article):
    return {
        "source": article["source"],
        "title": article["title"],
        "id": article["page_id"],
        "url": article["url"],
        "text": article["text"],
        "data": None
    }
def normalize_pokemon(pokemon):
    return {
        "source": "PokeAPI",
        "title": pokemon["name"],
        "id": pokemon["id"],
        "url": f"https://pokeapi.co/api/v2/pokemon/{pokemon['name'].lower()}",
        "text": None,
        "data": {
            "height": pokemon["height"],
            "weight": pokemon["weight"],
            "types": pokemon["types"],
            "abilities": pokemon["abilities"],
            "moves": pokemon["moves"]
        }
    }