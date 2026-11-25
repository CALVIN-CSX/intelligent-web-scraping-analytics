
import re
from collections import Counter


STOP_WORDS = {
    "the", "is", "in", "and", "a", "an", "of", "to",
    "for", "on", "with", "by", "as", "are", "was",
    "were", "it", "this", "that", "from", "be", "or",
    "at", "which", "has", "have", "its", "also", "their",
    "they", "them", "these", "those", "but", "not", "can",
    "could", "would", "should", "will", "shall", "may",
    "might", "must", "about", "into", "over", "under",
    "such", "than", "then", "there", "here", "when",
    "where", "while", "what", "who", "whom", "how",
    "why", "all", "any", "some", "more", "most", "other",
    "each", "both", "own", "same", "after", "before",
    "because", "through", "during", "without", "within",
    "between", "however", "therefore", "being", "been",
}


# Common webpage noise
NOISE_PATTERNS = [
    r"\bsubscribe\s+now\b",
    r"\bsign\s+in\b",
    r"\blog\s+in\b",
    r"\bsubscribe\s+to\s+our\s+newsletter\b",
    r"\bread\s+more\b",
    r"\bclick\s+here\b",
    r"\bskip\s+to\s+content\b",
    r"\bskip\s+navigation\b",
    r"\ball\s+rights\s+reserved\b",
    r"\bprivacy\s+policy\b",
    r"\bterms\s+of\s+use\b",
    r"\bcookie\s+policy\b",
    r"\baccept\s+cookies\b",
    r"\bmanage\s+cookies\b",
    r"\bshare\s+this\s+article\b",
    r"\brelated\s+articles\b",
    r"\btable\s+of\s+contents\b",
    r"\bback\s+to\s+top\b",
]


MIN_SENTENCE_WORDS = 5

MAX_ARTICLE_CHARACTERS = 30000


def clean_text(text):

    if not isinstance(text, str):
        return ""

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        "",
        text,
    )

    # Remove HTML-like tags if any remain
    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
    )

    # Remove unwanted control characters
    text = re.sub(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
        " ",
        text,
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def value_to_text(value):

    if isinstance(value, dict):

        if "name" in value:
            return value_to_text(value["name"])

        parts = []

        for key, nested_value in value.items():

            readable_value = value_to_text(
                nested_value
            )

            if readable_value:

                parts.append(
                    f"{key.replace('_', ' ')}: "
                    f"{readable_value}"
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

            readable_key = key.replace(
                "_",
                " ",
            )

            readable_value = value_to_text(
                value,
            )

            if readable_value:

                parts.append(
                    f"{readable_key}: "
                    f"{readable_value}"
                )

    return clean_text(
        ". ".join(parts)
    )


def tokenize(text):

    return re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower(),
    )


def extract_keywords(text, limit=8):

    words = [
        word
        for word in tokenize(text)
        if len(word) > 2
        and word not in STOP_WORDS
    ]

    return [
        word
        for word, count in Counter(
            words
        ).most_common(limit)
    ]


def split_sentences(text):

    text = re.sub(
        r"\s+",
        " ",
        text.strip(),
    )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def is_noise_sentence(sentence):

    sentence_lower = sentence.lower().strip()

    # Remove extremely short sentences
    if len(sentence.split()) < MIN_SENTENCE_WORDS:
        return True

    # Remove common website noise
    for pattern in NOISE_PATTERNS:

        if re.search(
            pattern,
            sentence_lower,
        ):
            return True

    # Remove menu-like fragments
    if sentence.count("|") >= 2:
        return True

    # Remove sentences consisting mainly of punctuation
    if not re.search(
        r"[a-zA-Z]{3,}",
        sentence,
    ):
        return True

    # Reject very long fragments that look like menu dumps
    if len(sentence.split()) > 100:
        return True

    return False


def clean_sentences(text):

    sentences = split_sentences(
        clean_text(text)
    )

    cleaned = []
    seen = set()

    for sentence in sentences:

        sentence = sentence.strip()

        if is_noise_sentence(sentence):
            continue

        normalized = sentence.lower()

        # Remove duplicate sentences
        if normalized in seen:
            continue

        seen.add(normalized)

        cleaned.append(sentence)

    return cleaned


def summarize_text(text, limit=3):

    sentences = clean_sentences(text)

    if not sentences:
        return ""

    if len(sentences) <= limit:
        return " ".join(sentences)

    keywords = set(
        extract_keywords(
            " ".join(sentences),
            limit=30,
        )
    )

    scored_sentences = []

    for index, sentence in enumerate(sentences):

        sentence_words = set(
            tokenize(sentence)
        )

        score = len(
            sentence_words.intersection(
                keywords
            )
        )

        # Prefer informative sentences
        word_count = len(
            sentence_words
        )

        if 10 <= word_count <= 35:
            score += 1

        scored_sentences.append(
            (
                score,
                index,
                sentence,
            )
        )

    best_sentences = sorted(
        scored_sentences,
        key=lambda item: (
            -item[0],
            item[1],
        ),
    )[:limit]

    # Restore original sentence order
    best_sentences.sort(
        key=lambda item: item[1]
    )

    return " ".join(
        sentence
        for score, index, sentence
        in best_sentences
    )


def build_excerpt(
    text,
    summary,
    limit=50,
):

    sentences = clean_sentences(
        text
    )

    summary_sentences = {
        sentence.lower().strip()
        for sentence in split_sentences(
            summary
        )
    }

    remaining_sentences = [
        sentence
        for sentence in sentences
        if sentence.lower().strip()
        not in summary_sentences
    ]

    preview = " ".join(
        remaining_sentences
    )

    return " ".join(
        preview.split()[:limit]
    )


def process_text(articles):

    processed_articles = []

    for original in articles:

        article = dict(original)

        raw_text = build_text(
            article
        )

        if not raw_text:

            processed_articles.append(
                article
            )

            continue

        # Limit processing size
        raw_text = raw_text[
            :MAX_ARTICLE_CHARACTERS
        ]

        # Clean and filter sentences
        sentences = clean_sentences(
            raw_text
        )

        cleaned_text = " ".join(
            sentences
        )

        if not cleaned_text:

            article["text"] = ""
            article["keywords"] = []
            article["word_count"] = 0
            article["summary"] = ""
            article["excerpt"] = ""

            processed_articles.append(
                article
            )

            continue

        article["text"] = cleaned_text

        article["keywords"] = (
            extract_keywords(
                cleaned_text,
            )
        )

        article["word_count"] = len(
            tokenize(cleaned_text)
        )

        article["summary"] = (
            summarize_text(
                cleaned_text,
            )
        )

        article["excerpt"] = (
            build_excerpt(
                cleaned_text,
                article["summary"],
            )
        )

        processed_articles.append(
            article
        )

    return processed_articles
