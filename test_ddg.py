
from app.sources.duckduckgo import search_duckduckgo

print("Starting DuckDuckGo test...")

results = search_duckduckgo(
    "advantages and disadvantages of renewable energy",
    limit=5,
)

print("\nTotal results:", len(results))

if not results:
    print("No results received.")

for result in results:

    print("\nTitle:", result["title"])
    print("URL:", result["url"])
    print("Text:", result["text"])

print("\nTest finished.")
