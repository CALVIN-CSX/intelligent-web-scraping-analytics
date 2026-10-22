from app.sources.wikipediaapi import search_wikipedia
from app.normalization.normalizer import normalize_wikipedia
from app.sources.pokeapi import get_pokemon_summary
from app.normalization.normalizer import normalize_pokemon
from app.nlp.processor import process_text

def search(query: str,source:str='wikipedia'):
    if source == "wikipedia":
        raw_results = search_wikipedia(query)

        normalized_results = [
            normalize_wikipedia(article)
            for article in raw_results
    ]

        return process_text(normalized_results)

    elif source == "pokemon":
        raw_results = get_pokemon_summary(query)
        return [
            normalize_pokemon(pokemon)
            for pokemon in raw_results
        ]
    else:
        raise ValueError(f"Unsupported source: {source}")