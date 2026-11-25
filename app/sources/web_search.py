# app/sources/web_search.py

from app.sources.duckduckgo import search_duckduckgo
from app.sources.webpage import extract_webpage


def search_web(query, limit=5):
    """
    Search one or multiple queries, collect search results,
    deduplicate URLs, and extract each unique webpage once.

    query can be:
        - a string
        - a list of strings
    """

    # Normalize query into a list
    if isinstance(query, str):
        queries = [query]
    else:
        queries = query

    # Step 1: Collect search results from all queries
    all_search_results = []

    for search_query in queries:
        try:
            search_results = search_duckduckgo(
                search_query,
                limit=limit
            )

            if search_results:
                all_search_results.extend(search_results)

        except Exception as e:
            print(f"Search error for '{search_query}': {e}")

    # Step 2: Deduplicate URLs BEFORE extracting webpages
    unique_results = []
    seen_urls = set()

    for result in all_search_results:

        url = result.get("url", "").strip()

        if not url:
            continue

        # Skip DuckDuckGo redirect links
        if "aclick" in url.lower():
            continue

        # Remove duplicate URLs
        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_results.append(result)

    # Step 3: Extract each unique webpage only once
    articles = []

    for result in unique_results:

        url = result.get("url", "").strip()
        title = result.get("title", "")
        snippet = result.get("text", "")

        try:
            webpage = extract_webpage(url)

            if webpage and webpage.get("text", "").strip():

                webpage["title"] = webpage.get("title") or title
                webpage["url"] = webpage.get("url") or url
                webpage["source"] = "duckduckgo"

                articles.append(webpage)

            else:
                # Fallback to search snippet
                articles.append({
                    "title": title,
                    "url": url,
                    "text": snippet,
                    "source": "duckduckgo"
                })

        except Exception as e:

            print(f"Webpage extraction error for {url}: {e}")

            # Fallback to search snippet
            articles.append({
                "title": title,
                "url": url,
                "text": snippet,
                "source": "duckduckgo"
            })

    return articles