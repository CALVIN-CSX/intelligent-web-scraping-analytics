
from app.query_understanding.parser import parse_query
from app.query_understanding.expander import expand_query
from app.retrieval.ranker import rank_articles
from app.answer_generation.generator import generate_answer


query = "Some important concepts on machine learning"

# Step 1: Understand query
parsed = parse_query(query)

print("\nPARSED QUERY")
print(parsed)

# Step 2: Expand query
expanded = expand_query(parsed)

print("\nEXPANDED QUERIES")

for item in expanded:
    print("-", item)

# Step 3: Sample articles
articles = [
    {
        "title": "Machine Learning",
        "summary": "Machine learning enables computers to learn patterns from data.",
        "url": "https://example.com/ml"
    },
    {
        "title": "Supervised Learning",
        "summary": "Supervised learning uses labelled training data to make predictions.",
        "url": "https://example.com/supervised"
    },
    {
        "title": "Cooking",
        "summary": "Cooking is the process of preparing food.",
        "url": "https://example.com/cooking"
    }
]

# Step 4: Rank articles
ranked = rank_articles(articles, parsed)
print("\nRANKED ARTICLES")

for article in ranked:
    print("\nTitle:", article["title"])
    print("Keyword Score:", article["keyword_score"])
    print("Semantic Score:", article["semantic_score"])
    print("Final Score:", article["relevance_score"])
# Step 5: Generate answer
answer = generate_answer(ranked, parsed)

print("\nCONSOLIDATED ANSWER")
print(answer)
