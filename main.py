from app.sources.pokeapi import get_pokemon_summary
from app.sources.wikipediaapi import search_wikipedia,search_output
from app.normalization.normalizer import normalize_wikipedia,normalize_pokemon
from app.presentation.display import display
def result():
    print("which api do you want?\n1.wekipedia\n2.pokeapi")
    api = input()
    if api == "1":
        query = input("Topic name: ")
        articles=search_wikipedia(query)

        normalized_wiki = [
            normalize_wikipedia(article)
            for article in articles
        ]
        return normalized_wiki
    else:
        name = input("Enter pokemon name: ") or "pikachu"
        pokemon=get_pokemon_summary(name)
        normalized_pokemon = [
            normalize_pokemon(p)
            for p in pokemon
        ]
        return normalized_pokemon
data=result()
display(data)
