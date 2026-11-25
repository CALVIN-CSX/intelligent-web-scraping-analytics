
import re
from sentence_transformers import SentenceTransformer, util


print("Loading semantic ranking model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


STOP_WORDS = {
    "the", "is", "a", "an", "of", "in",
    "on", "and", "or", "to", "for", "with",
    "what", "how", "why", "some", "important",
    "about", "explain", "find", "give", "me"
}


def tokenize(text):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        str(text).lower()
    )

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    }


def get_article_text(article):

    fields = [
        article.get("title", ""),
        article.get("summary", ""),
        article.get("excerpt", ""),
        article.get("text", "")
    ]

    return " ".join(
        str(value) for value in fields if value
    )


def rank_articles(articles, parsed_query):

    if not articles:
        return []

    topic = parsed_query["topic"]

    query_embedding = model.encode(
        topic,
        convert_to_tensor=True
    )

    article_texts = [
        get_article_text(article)
        for article in articles
    ]

    article_embeddings = model.encode(
        article_texts,
        convert_to_tensor=True
    )

    semantic_scores = util.cos_sim(
        query_embedding,
        article_embeddings
    )[0]

    query_words = tokenize(topic)

    ranked_articles = []

    for index, article in enumerate(articles):

        title = str(article.get("title", ""))
        summary = str(article.get("summary", ""))

        article_text = article_texts[index]

        title_words = tokenize(title)
        summary_words = tokenize(summary)
        article_words = tokenize(article_text)

        # Keyword score
        keyword_score = 0

        keyword_score += len(query_words & title_words) * 5
        keyword_score += len(query_words & summary_words) * 3
        keyword_score += len(query_words & article_words) * 2

        if topic.lower() in title.lower():
            keyword_score += 10

        # Normalize keyword score to 0-1
        normalized_keyword_score = (
            keyword_score / (keyword_score + 10)
            if keyword_score > 0
            else 0
        )

        # Semantic score
        semantic_score = float(
            semantic_scores[index].item()
        )

        # Clamp semantic score to 0-1
        normalized_semantic_score = max(
            0,
            min(semantic_score, 1)
        )

        # Combine normalized scores
        final_score = (
            0.4 * normalized_keyword_score
            + 0.6 * normalized_semantic_score
        )

        result = article.copy()

        result["keyword_score"] = keyword_score
        result["normalized_keyword_score"] = round(
            normalized_keyword_score, 4
        )
        result["semantic_score"] = round(
            semantic_score, 4
        )
        result["relevance_score"] = round(
            final_score, 4
        )

        ranked_articles.append(result)

    ranked_articles.sort(
        key=lambda item: item["relevance_score"],
        reverse=True
    )

    # Filter irrelevant articles
    ranked_articles = [
        article for article in ranked_articles
        if article["keyword_score"] > 0
        or article["semantic_score"] >= 0.25
    ]

    return ranked_articles
