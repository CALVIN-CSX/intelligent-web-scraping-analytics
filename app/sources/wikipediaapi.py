import requests
def search_wikipedia(query : str):
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query
    }

    HEADERS = {
        "User-Agent": "IntelligentWebScrapingAnalytics/1.0 (https://github.com/CALVIN-CSX/intelligent-web-scraping-analytics)"
    }

    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS
    )
    data = response.json()
    page_ids = [
        result["pageid"]
        for result in data["query"]["search"]
    ]
    PARAMS = {
        "action": "query",
        "format": "json",
        "pageids": "|".join(map(str, page_ids)),
        "prop": "extracts",
        "explaintext": True,
        "exintro": True,
    }
    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS
    )
    tdata = response.json()
    articles = []

    for page in tdata["query"]["pages"].values():
        articles.append({
            "title": page["title"],
            "text": page.get("extract", ""),
            "source": "Wikipedia",
            "page_id": page["pageid"],
            "url": f"https://en.wikipedia.org/?curid={page['pageid']}"
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

