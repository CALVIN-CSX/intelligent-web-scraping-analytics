# app/sources/duckduckgo.py

import re
from ddgs import DDGS


def clean_text(text):
    """Clean whitespace and unwanted characters from text."""

    if not text:
        return ""

    text = str(text)

    # Remove HTML-like tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def search_duckduckgo(query, limit=5):
    """
    Search DuckDuckGo and return cleaned, unique results.

    Each result contains:
        title
        url
        text
        source
    """

    results = []
    seen_urls = set()

    try:

        with DDGS(timeout=15) as ddgs:

            search_results = ddgs.text(
                query,
                max_results=limit,
            )

            if not search_results:
                return results

            for item in search_results:

                # Extract raw fields
                title = clean_text(item.get("title", ""))
                url = clean_text(item.get("href", ""))
                snippet = clean_text(item.get("body", ""))

                # Skip unusable results
                if not url:
                    continue

                if url in seen_urls:
                    continue

                if not title and not snippet:
                    continue

                seen_urls.add(url)

                results.append({
                    "title": title,
                    "url": url,
                    "text": snippet,
                    "source": "duckduckgo",
                })

                # Respect requested result limit
                if len(results) >= limit:
                    break

    except Exception as e:

        print(f"DuckDuckGo search error: {e}")

        return results

    return results