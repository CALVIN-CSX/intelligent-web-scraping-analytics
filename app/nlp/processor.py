
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


def value_to_text(value):
    if isinstance(value, dict):
        if "name" in value:
            return value_to_text(value["name"])

        parts = []

        for key, nested_value in value.items():
            readable_value = value_to_text(nested_value)

            if readable_value:
                parts.append(
                    f"{key.replace('_', ' ')}: {readable_value}"
                )

        return ", ".join(parts)

    if isinstance(value, list):
        parts = [
            value_to_text(item)
            for item in value
        ]

        return ", ".join(
            part for part in parts if part
        )

    if value is None:
        return ""

    return str(value)


def build_text(article):
    parts = []

    existing_text = article.get("text")

    if isinstance(existing_text, str):
        parts.append(existing_text)

    data = article.get("data")

    if isinstance(data, dict):
        for key, value in data.items():
            readable_key = key.replace("_", " ")
            readable_value = value_to_text(value)

            if readable_value:
                parts.append(
                    f"{readable_key}: {readable_value}"
                )

    return clean_text(". ".join(parts))


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



def split_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def summarize_text(text, limit=2):
    sentences = split_sentences(text)

    if len(sentences) <= limit:
        return " ".join(sentences)

    keywords = set(extract_keywords(text))

    scored_sentences = []

    for index, sentence in enumerate(sentences):
        sentence_words = set(tokenize(sentence))

        score = len(sentence_words & keywords)

        scored_sentences.append(
            (score, index, sentence)
        )

    best_sentences = sorted(
        scored_sentences,
        key=lambda item: (-item[0], item[1])
    )[:limit]

    best_sentences.sort(
        key=lambda item: item[1]
    )

    return " ".join(
        sentence
        for score, index, sentence in best_sentences
    )


def build_excerpt(text, summary, limit=35):
    sentences = split_sentences(text)

    # Normalize summary sentences for comparison
    summary_sentences = {
        sentence.lower().strip()
        for sentence in split_sentences(summary)
    }

    # Remove sentences already displayed in the summary
    remaining_sentences = [
        sentence
        for sentence in sentences
        if sentence.lower().strip() not in summary_sentences
    ]

    # Use only the remaining article content
    preview = " ".join(remaining_sentences)

    return " ".join(preview.split()[:limit])



def process_text(articles):
    processed_articles = []

    for original in articles:
        article = dict(original)

        text = build_text(article)

        if not text:
            processed_articles.append(article)
            continue

        article["text"] = text

        article["keywords"] = extract_keywords(text)

        article["word_count"] = len(
            tokenize(text)
        )

        article["summary"] = summarize_text(text)

        article["excerpt"] = build_excerpt(
            text,
            article["summary"]
        )

        processed_articles.append(article)

    return processed_articles
