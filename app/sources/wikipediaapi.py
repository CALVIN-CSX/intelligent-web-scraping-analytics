
import requests


def search_wikipedia(query: str, limit: int = 20):
    URL = "https://en.wikipedia.org/w/api.php"

    HEADERS = {
        "User-Agent": (
            "IntelligentWebScrapingAnalytics/1.0 "
            "(https://github.com/CALVIN-CSX/"
            "intelligent-web-scraping-analytics)"
        )
    }

    # Request 1: Search for Wikipedia articles
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
    }

    response = requests.get(
        URL,
        params=search_params,
        headers=HEADERS,
        timeout=15,
    )

    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(
            f"Wikipedia search error: {data['error']}"
        )

    if "query" not in data:
        raise RuntimeError(
            f"Unexpected Wikipedia search response: {data}"
        )

    page_ids = [
        result["pageid"]
        for result in data["query"]["search"]
    ]

    # No articles found
    if not page_ids:
        return []

    # Request 2: Fetch the article text
    article_params = {
        "action": "query",
        "format": "json",
        "pageids": "|".join(map(str, page_ids)),
        "prop": "extracts",
        "explaintext": True,
        "exintro": True,
    }

    response = requests.get(
        URL,
        params=article_params,
        headers=HEADERS,
        timeout=15,
    )

    response.raise_for_status()
    tdata = response.json()

    if "error" in tdata:
        raise RuntimeError(
            f"Wikipedia article error: {tdata['error']}"
        )

    if "query" not in tdata or "pages" not in tdata["query"]:
        raise RuntimeError(
            f"Unexpected Wikipedia article response: {tdata}"
        )

    articles = []

    for page in tdata["query"]["pages"].values():
        articles.append({
            "title": page["title"],
            "text": page.get("extract", ""),
            "source": "Wikipedia",
            "page_id": page["pageid"],
            "url": (
                f"https://en.wikipedia.org/"
                f"?curid={page['pageid']}"
            ),
        })

    return articles


def search_output(articles: list):
    for i, article in enumerate(articles, start=1):
        print(f"\nArticle: {i}.")
        print(f"Title: {article['title']}")
        print(f"Text: {article['text']}")
        print(f"Source: {article['source']}")
        print(f"Page ID: {article['page_id']}")
        print(f"URL: {article['url']}")
