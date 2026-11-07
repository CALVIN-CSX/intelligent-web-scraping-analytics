
from app.sources.wikipediaapi import search_wikipedia
from app.normalization.normalizer import normalize_wikipedia

from app.sources.pokeapi import get_pokemon_summary
from app.normalization.normalizer import normalize_pokemon

from app.nlp.processor import process_text


def search(
    query: str,
    source: str = "wikipedia",
    limit: int = 20,
):

    if source == "wikipedia":

        # Retrieve the requested number of Wikipedia articles
        raw_results = search_wikipedia(
            query,
            limit=limit,
        )

        normalized_results = [
            normalize_wikipedia(article)
            for article in raw_results
        ]

    elif source == "pokemon":

        # Retrieve Pokémon information
        raw_results = get_pokemon_summary(query)

        normalized_results = [
            normalize_pokemon(pokemon)
            for pokemon in raw_results
        ]

    else:
        raise ValueError(
            f"Unsupported source: {source}"
        )

    # Apply NLP processing to all retrieved results
    return process_text(normalized_results)
