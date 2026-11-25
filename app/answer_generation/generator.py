
import re
from collections import Counter


MAX_SENTENCES = 12
MIN_WORDS_PER_SENTENCE = 7
MAX_SENTENCE_WORDS = 65


# -------------------------------------------------------------------
# 1. Sentence classification vocabulary
# -------------------------------------------------------------------

ADVANTAGE_PATTERNS = [
    r"\bbenefit(s)?\b",
    r"\badvantage(s)?\b",
    r"\bimprov(e|es|ed|ement|ements)\b",
    r"\befficient|efficiency\b",
    r"\bpositive impact(s)?\b",
    r"\bstrength(s)?\b",
    r"\bhelp(s)?\b",
    r"\bsupport(s)?\b",
    r"\breduc(e|es|ed|ing)\b",
    r"\blower(s|ed|ing)?\b",
    r"\bsave(s|d|ing)?\b",
    r"\bcheaper\b",
    r"\bcost-effective\b",
    r"\bcleaner\b",
    r"\bsustainable\b",
    r"\bprotect(s|ing)?\b",
    r"\bdecreas(e|es|ed|ing)\b",
    r"\bboost(s|ed|ing)?\b",
    r"\bincreas(e|es|ed|ing)\b",
    r"\bcreate(s|d)? jobs\b",
    r"\bjob creation\b",
    r"\bsecure\b",
    r"\breliable\b",
    r"\bpromot(e|es|ed|ing)\b",
    r"\bcontribut(e|es|ed|ing)\b",
    r"\bmitigat(e|es|ed|ing)\b",
    r"\bdiversif(y|ies|ied|ication)\b",
    r"\bpreserv(e|es|ed|ing)\b",
    r"\badvantages of\b",
    r"\bpotential to\b",
    r"\bopportunit(y|ies)\b",
]

DISADVANTAGE_PATTERNS = [
    r"\bdisadvantage(s)?\b",
    r"\bdrawback(s)?\b",
    r"\blimitation(s)?\b",
    r"\bnegative impact(s)?\b",
    r"\bproblem(s)?\b",
    r"\brisk(s)?\b",
    r"\bweakness(es)?\b",
    r"\bharm(s|ful)?\b",
    r"\bdifficult(y|ies)?\b",
    r"\bexpensive\b",
    r"\bcostly\b",
    r"\bhigh cost(s)?\b",
    r"\bpoor\b",
    r"\bunreliable\b",
    r"\bintermittent\b",
    r"\bvariab(le|ility)\b",
    r"\bdepend(s|ent|ence)? on\b",
    r"\bshortage(s)?\b",
    r"\bchallenge(s)?\b",
    r"\bcomplicat(e|es|ed|ions)\b",
    r"\bdisrupt(s|ed|ion)?\b",
    r"\bdegrad(e|es|ed|ation)\b",
    r"\bpollut(e|es|ion|ants|ed)\b",
    r"\bimpact(s)? on\b",
    r"\btrade-off(s)?\b",
    r"\btradeoff(s)?\b",
    r"\bdisadvantage of\b",
    r"\bbarrier(s)?\b",
    r"\bobstacle(s)?\b",
    r"\bmaintenance\b",
    r"\bsubsid(y|ies)\b",
    r"\bscarce\b",
    r"\bscarcity\b",
    r"\bconflict(s)?\b",
    r"\bconstrain(s|ed|t)?\b",
    r"\bdependence\b",
]


# -------------------------------------------------------------------
# 2. Noise filtering
# -------------------------------------------------------------------

NOISE_PATTERNS = [
    r"\bsubscribe\b",
    r"\bsign in\b",
    r"\blog in\b",
    r"\bnewsletter\b",
    r"\bread more\b",
    r"\bclick here\b",
    r"\bskip to content\b",
    r"\bskip navigation\b",
    r"\ball rights reserved\b",
    r"\bprivacy policy\b",
    r"\bterms of use\b",
    r"\bcookie policy\b",
    r"\baccept cookies\b",
    r"\bmanage cookies\b",
    r"\bshare this article\b",
    r"\brelated articles\b",
    r"\btable of contents\b",
    r"\bback to top\b",
    r"\bon this page\b",
    r"\bfrequently asked questions\b",
    r"\bwritten by\b",
    r"\bfact.check(ed)? by\b",
    r"\blast updated\b",
    r"\bends soon\b",
    r"\bplus for\b",
    r"\bclick to\b",
    r"\bwatch now\b",
    r"\bdownload now\b",
    r"\bshop now\b",
    r"\badvertisement\b",
    r"\bsponsored content\b",
    r"\bget started today\b",
]


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


# -------------------------------------------------------------------
# 3. Basic utilities
# -------------------------------------------------------------------

def get_article_content(article):

    return (
        article.get("text")
        or article.get("summary")
        or article.get("excerpt")
        or ""
    )


def split_sentences(text):

    if not isinstance(text, str):
        return []

    text = re.sub(
        r"\s+",
        " ",
        text.strip(),
    )

    if not text:
        return []

    return [
        sentence.strip()
        for sentence in re.split(
            r"(?<=[.!?])\s+",
            text,
        )
        if sentence.strip()
    ]


def tokenize(text):

    return set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )
    )


def topic_keywords(topic):

    return {
        word
        for word in re.findall(
            r"\b[a-zA-Z0-9]+\b",
            topic.lower(),
        )
        if word not in STOP_WORDS
        and len(word) > 2
    }


# -------------------------------------------------------------------
# 4. Noise detection
# -------------------------------------------------------------------

def is_noise_sentence(sentence):

    sentence = sentence.strip()
    lower = sentence.lower()

    words = sentence.split()

    # Very short or excessively long sentences
    if len(words) < MIN_WORDS_PER_SENTENCE:
        return True

    if len(words) > MAX_SENTENCE_WORDS:
        return True

    # Promotional, navigation or boilerplate text
    for pattern in NOISE_PATTERNS:

        if re.search(
            pattern,
            lower,
        ):
            return True

    # Citation fragments
    if re.match(
        r"^\[\s*\d+\s*\]",
        sentence,
    ):
        return True

    # Navigation or list fragments
    if sentence.count("|") >= 2:
        return True

    # Sentences with too many non-word characters
    if len(
        re.findall(
            r"[a-zA-Z]",
            sentence,
        )
    ) < 10:
        return True

    # Remove excessively repetitive text
    word_list = re.findall(
        r"\b[a-zA-Z]+\b",
        lower,
    )

    if word_list:

        repeated_ratio = (
            len(set(word_list))
            / len(word_list)
        )

        if repeated_ratio < 0.25:
            return True

    return False


def clean_sentence(sentence):

    sentence = re.sub(
        r"\[\s*\d+\s*\]",
        "",
        sentence,
    )

    sentence = re.sub(
        r"\s+",
        " ",
        sentence,
    )

    sentence = sentence.strip()

    return sentence


# -------------------------------------------------------------------
# 5. Relevance scoring
# -------------------------------------------------------------------

def sentence_relevance(sentence, topic):

    topic_words = topic_keywords(topic)

    sentence_words = tokenize(sentence)

    if not topic_words:
        return 0.0

    overlap = topic_words.intersection(
        sentence_words
    )

    # Proportional overlap, not a fixed saturated score
    overlap_score = (
        len(overlap)
        / len(topic_words)
    )

    # Exact phrase bonus
    phrase_bonus = 0.0

    if topic.lower() in sentence.lower():
        phrase_bonus = 0.35

    # Partial phrase bonus
    partial_bonus = 0.0

    if len(topic_words) > 1:

        if len(overlap) >= 2:
            partial_bonus = 0.10

    # Prefer sentences with informative length
    length_bonus = 0.0

    word_count = len(
        sentence.split()
    )

    if 12 <= word_count <= 35:
        length_bonus = 0.05

    score = (
        overlap_score
        + phrase_bonus
        + partial_bonus
        + length_bonus
    )

    return round(
        score,
        4,
    )


# -------------------------------------------------------------------
# 6. Intent classification
# -------------------------------------------------------------------

def pattern_score(sentence, patterns):

    score = 0

    lower = sentence.lower()

    for pattern in patterns:

        if re.search(
            pattern,
            lower,
        ):
            score += 1

    return score


def classify_sentence(sentence):

    advantage_score = pattern_score(
        sentence,
        ADVANTAGE_PATTERNS,
    )

    disadvantage_score = pattern_score(
        sentence,
        DISADVANTAGE_PATTERNS,
    )

    # Avoid classifying sentences as negative just because
    # they contain the word "challenge" in a neutral context.
    if advantage_score > disadvantage_score:
        return "advantages"

    if disadvantage_score > advantage_score:
        return "disadvantages"

    return "neutral"


# -------------------------------------------------------------------
# 7. Candidate collection
# -------------------------------------------------------------------

def collect_sentences(articles, topic):

    candidates = []
    seen_sentences = set()

    for article_index, article in enumerate(articles):

        content = get_article_content(
            article
        )

        if not content:
            continue

        sentences = split_sentences(
            content
        )

        for sentence_index, sentence in enumerate(sentences):

            sentence = clean_sentence(
                sentence
            )

            if is_noise_sentence(
                sentence
            ):
                continue

            normalized = re.sub(
                r"\s+",
                " ",
                sentence.lower(),
            ).strip()

            if normalized in seen_sentences:
                continue

            seen_sentences.add(
                normalized
            )

            relevance = sentence_relevance(
                sentence,
                topic,
            )

            if relevance <= 0:
                continue

            candidates.append({
                "sentence": sentence,
                "score": relevance,
                "article_index": article_index,
                "sentence_index": sentence_index,
                "article": article,
                "classification": classify_sentence(
                    sentence
                ),
            })

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return candidates


# -------------------------------------------------------------------
# 8. Balanced selection
# -------------------------------------------------------------------

def select_sentences(
    candidates,
    limit=MAX_SENTENCES,
    intent="general",
):

    selected = []
    used_sentences = set()
    article_counts = Counter()

    # Allow a maximum of 3 sentences from one article initially
    MAX_PER_ARTICLE = 3

    # Combined intent: first attempt to balance both sides
    if intent == "advantages_disadvantages":

        for category in [
            "advantages",
            "disadvantages",
        ]:

            category_candidates = [
                item
                for item in candidates
                if item["classification"] == category
            ]

            for item in category_candidates:

                sentence = item["sentence"]
                article_index = item["article_index"]

                if sentence in used_sentences:
                    continue

                if article_counts[article_index] >= MAX_PER_ARTICLE:
                    continue

                selected.append(item)
                used_sentences.add(sentence)
                article_counts[article_index] += 1

                if len(selected) >= limit:
                    return selected

                # Initially target a few sentences from each side
                category_count = sum(
                    1
                    for chosen in selected
                    if chosen["classification"] == category
                )

                if category_count >= max(
                    2,
                    limit // 4,
                ):
                    break

    # Fill remaining spaces with highest-scoring sentences
    for item in candidates:

        sentence = item["sentence"]
        article_index = item["article_index"]

        if sentence in used_sentences:
            continue

        if article_counts[article_index] >= MAX_PER_ARTICLE:
            continue

        selected.append(item)
        used_sentences.add(sentence)
        article_counts[article_index] += 1

        if len(selected) >= limit:
            break

    return selected


# -------------------------------------------------------------------
# 9. Source formatting
# -------------------------------------------------------------------

def format_sources(selected):

    sources = []
    seen_urls = set()

    for item in selected:

        article = item["article"]

        url = article.get(
            "url",
            "",
        )

        if url and url in seen_urls:
            continue

        if url:
            seen_urls.add(url)

        sources.append({
            "title": article.get(
                "title",
                "Untitled",
            ),
            "url": url,
        })

    if not sources:
        return ""

    output = "\n\nSources:\n"

    for source in sources:

        output += (
            "- "
            + source["title"]
        )

        if source["url"]:
            output += (
                " ("
                + source["url"]
                + ")"
            )

        output += "\n"

    return output


# -------------------------------------------------------------------
# 10. Answer formatting
# -------------------------------------------------------------------

def format_combined_answer(
    selected,
    topic,
):

    advantages = []
    disadvantages = []
    neutral = []

    for item in selected:

        sentence = item["sentence"]

        classification = item[
            "classification"
        ]

        if classification == "advantages":

            advantages.append(
                sentence
            )

        elif classification == "disadvantages":

            disadvantages.append(
                sentence
            )

        else:

            neutral.append(
                sentence
            )

    answer = (
        f"Overview of {topic}:\n\n"
    )

    if advantages:

        answer += "Advantages:\n"

        for sentence in advantages:

            answer += (
                "- "
                + sentence
                + "\n"
            )

        answer += "\n"

    if disadvantages:

        answer += "Disadvantages:\n"

        for sentence in disadvantages:

            answer += (
                "- "
                + sentence
                + "\n"
            )

        answer += "\n"

    if neutral:

        answer += "Additional information:\n"

        for sentence in neutral:

            answer += (
                "- "
                + sentence
                + "\n"
            )

    return answer.strip()


# -------------------------------------------------------------------
# 11. Main generator
# -------------------------------------------------------------------

def generate_answer(
    articles,
    parsed_query,
):

    if not articles:

        return (
            "No relevant information was found."
        )

    topic = parsed_query.get(
        "topic",
        "the searched topic",
    )

    intent = parsed_query.get(
        "intent",
        "general",
    )

    candidates = collect_sentences(
        articles,
        topic,
    )

    if not candidates:

        return (
            "Relevant articles were found, "
            "but they did not contain enough "
            "relevant information to generate "
            "an answer."
        )

    selected = select_sentences(
        candidates,
        limit=MAX_SENTENCES,
        intent=intent,
    )

    if intent == "advantages_disadvantages":

        answer = format_combined_answer(
            selected,
            topic,
        )

    else:

        answer = (
            f"Overview of {topic}:\n\n"
        )

        answer += "\n".join(
            "- "
            + item["sentence"]
            for item in selected
        )

    answer += format_sources(
        selected
    )

    return answer
