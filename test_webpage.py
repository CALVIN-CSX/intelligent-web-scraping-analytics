
print("Starting webpage extraction test...")

from app.sources.webpage import extract_webpage

print("Import successful!")

url = "https://www.energysage.com/about-clean-energy/advantages-and-disadvantages-of-renewable-energy/"

print("Attempting to fetch webpage...")

article = extract_webpage(url)

print("\nReturned value:", article is not None)

if article:

    print("\nTitle:", article["title"])
    print("\nURL:", article["url"])
    print("\nExtracted text:\n")
    print(article["text"][:3000])

else:

    print("\nCould not extract webpage content.")

print("\nTest finished.")
