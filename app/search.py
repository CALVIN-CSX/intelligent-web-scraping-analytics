from app.sources.wikipediaapi import search_wikipedia
from app.normalization.normalizer import normalize_wikipedia

from app.sources.pokeapi import get_pokemon_summary
from app.normalization.normalizer import normalize_pokemon

from app.sources.web_search import search_web

from app.nlp.processor import process_text

from app.query_understanding.parser import parse_query
from app.query_understanding.expander import expand_query

from app.retrieval.ranker import rank_articles
from app.answer_generation.generator import generate_answer


def search(
    query: str,
    source: str = "wikipedia",
    limit: int = 20,
):

    # 1. Understand the query
    parsed_query = parse_query(query)

    # 2. Retrieve data from the selected source

    if source == "wikipedia":

        expanded_queries = expand_query(parsed_query)

        if not expanded_queries:
            expanded_queries = [query]

        raw_results = []
        seen_titles = set()

        for expanded_query in expanded_queries:

            results = search_wikipedia(
                expanded_query,
                limit=max(
                    5,
                    limit // len(expanded_queries),
                ),
            )

            for article in results:

                title = article.get("title", "")

                if title not in seen_titles:
                    seen_titles.add(title)
                    raw_results.append(article)

        normalized_results = [
            normalize_wikipedia(article)
            for article in raw_results
        ]

    elif source == "web":

        # Expand the original query
        expanded_queries = expand_query(parsed_query)

        if not expanded_queries:
            expanded_queries = [query]

        # Calculate search result limit per expanded query
        search_limit = max(
            3,
            limit // len(expanded_queries),
        )

        # Search all expanded queries together
        # search_web now collects results first,
        # deduplicates URLs, then extracts webpages.

        raw_results = search_web(
            expanded_queries,
            limit=search_limit,
        )

        # Web results already contain title, url and text
        normalized_results = raw_results

    elif source == "pokemon":

        raw_results = get_pokemon_summary(query)

        normalized_results = [
            normalize_pokemon(pokemon)
            for pokemon in raw_results
        ]

        expanded_queries = [query]

    else:

        raise ValueError(
            f"Unsupported source: {source}"
        )

    # 3. Process retrieved text using NLP
    processed_results = process_text(
        normalized_results
    )

    # 4. Rank articles
    ranked_results = rank_articles(
        processed_results,
        parsed_query,
    )

    # 5. Generate answer
    answer = generate_answer(
        ranked_results,
        parsed_query,
    )

    # 6. Return complete response
    return {
        "query": query,
        "parsed_query": parsed_query,
        "expanded_queries": expanded_queries,
        "answer": answer,
        "results": ranked_results[:limit],
    }