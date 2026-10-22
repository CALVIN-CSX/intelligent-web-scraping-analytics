
import re
from collections import Counter

STOP_WORDS = {
    "the", "is", "in", "and", "a", "an", "of", "to",
    "for", "on", "with", "by", "as", "are", "was",
    "were", "it", "this", "that", "from", "be", "or",
    "at", "which", "has", "have", "its", "also"
}


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def extract_keywords(text, limit=8):
    words = [
        word for word in tokenize(text)
        if len(word) > 2 and word not in STOP_WORDS
    ]

    return [
        word for word, count in Counter(words).most_common(limit)
    ]


def process_text(articles):
    processed_articles = []

    for original in articles:
        article = dict(original)
        text = clean_text(article.get("text"))

        if not text:
            processed_articles.append(article)
            continue

        article["text"] = text
        article["keywords"] = extract_keywords(text)
        article["word_count"] = len(tokenize(text))
        article["excerpt"] = " ".join(text.split()[:35])

        processed_articles.append(article)

    return processed_articles
