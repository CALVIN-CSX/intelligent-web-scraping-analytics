
import re


INTENT_PATTERNS = {
    "advantages_disadvantages": [
        r"\badvantages?\s+and\s+disadvantages?\b",
        r"\bpros\s+and\s+cons\b",
        r"\bbenefits?\s+and\s+drawbacks?\b",
        r"\bstrengths?\s+and\s+weaknesses?\b",
    ],

    "comparison": [
        r"\bcompare\b",
        r"\bcomparison\b",
        r"\bdifference(?:s)? between\b",
        r"\bversus\b",
        r"\bvs\.?\b",
    ],

    "advantages": [
        r"\badvantages?\b",
        r"\bbenefits?\b",
        r"\bpros\b",
    ],

    "disadvantages": [
        r"\bdisadvantages?\b",
        r"\bdrawbacks?\b",
        r"\blimitations?\b",
        r"\bcons\b",
        r"\bchallenges?\b",
    ],

    "concepts": [
        r"\bimportant concepts?\b",
        r"\bkey concepts?\b",
        r"\bimportant topics?\b",
        r"\bkey topics?\b",
        r"\bfundamentals\b",
        r"\bbasics\b",
        r"\bconcepts?\b",
    ],

    "types": [
        r"\btypes? of\b",
        r"\bcategories of\b",
        r"\bkinds of\b",
    ],

    "latest": [
        r"\blatest\b",
        r"\brecent developments\b",
        r"\bcurrent trends\b",
        r"\bnew developments\b",
    ],

    "explanation": [
        r"\bexplain\b",
        r"\bdescribe\b",
        r"\bhow does\b",
        r"\bhow do\b",
        r"\bhow it works\b",
        r"\bwhat is\b",
        r"\bwhat are\b",
    ],
}


def detect_intent(query):

    query_lower = query.lower()

    # Detect combined intent first
    for pattern in INTENT_PATTERNS["advantages_disadvantages"]:

        if re.search(pattern, query_lower):
            return "advantages_disadvantages"

    # Detect other intents
    for intent, patterns in INTENT_PATTERNS.items():

        if intent == "advantages_disadvantages":
            continue

        for pattern in patterns:

            if re.search(pattern, query_lower):
                return intent

    return "general"


def extract_topic(query, intent):

    topic = query.lower().strip()

    # Remove common question beginnings
    prefixes = [
        r"^(?:please\s+)?",
        r"^(?:can you|could you|would you)\s+",
        r"^(?:tell me|show me|give me|find me)\s+",
        r"^(?:what\s+(?:are|is)|how\s+(?:does|do)|why\s+(?:is|does))\s+",
    ]

    for pattern in prefixes:

        topic = re.sub(
            pattern,
            "",
            topic,
            count=1,
        )

    # Remove phrases associated with detected intent
    removal_patterns = {

        "advantages_disadvantages": [
            r"\badvantages?\s+and\s+disadvantages?\b",
            r"\bpros\s+and\s+cons\b",
            r"\bbenefits?\s+and\s+drawbacks?\b",
            r"\bstrengths?\s+and\s+weaknesses?\b",
        ],

        "concepts": [
            r"\b(?:some\s+)?(?:important|key)\s+concepts?\b",
            r"\b(?:some\s+)?(?:important|key)\s+topics?\b",
            r"\bconcepts?\b",
            r"\bfundamentals\b",
            r"\bbasics\b",
        ],

        "comparison": [
            r"\bcompare\b",
            r"\bcomparison\b",
            r"\bdifferences?\s+between\b",
            r"\bversus\b",
            r"\bvs\.?\b",
        ],

        "advantages": [
            r"\badvantages?\b",
            r"\bbenefits?\b",
            r"\bpros\b",
        ],

        "disadvantages": [
            r"\bdisadvantages?\b",
            r"\bdrawbacks?\b",
            r"\blimitations?\b",
            r"\bchallenges?\b",
            r"\bcons\b",
        ],

        "types": [
            r"\btypes?\s+of\b",
            r"\bcategories\s+of\b",
            r"\bkinds\s+of\b",
        ],

        "latest": [
            r"\blatest\s+developments\b",
            r"\brecent\s+developments\b",
            r"\bcurrent\s+trends\b",
            r"\bnew\s+developments\b",
            r"\blatest\b",
            r"\brecent\b",
            r"\bcurrent\b",
        ],

        "explanation": [
            r"\bexplain\b",
            r"\bdescribe\b",
            r"\bwhat\s+is\b",
            r"\bwhat\s+are\b",
            r"\bhow\s+does\b",
            r"\bhow\s+do\b",
            r"\bhow\s+it\s+works\b",
        ],
    }

    # Remove detected intent phrases
    for pattern in removal_patterns.get(intent, []):

        topic = re.sub(
            pattern,
            " ",
            topic,
        )

    # Remove conversational filler words
    filler_words = {
        "some",
        "the",
        "a",
        "an",
        "on",
        "about",
        "of",
        "for",
        "please",
        "me",
        "to",
        "in",
        "and",
        "is",
        "are",
        "by",
        "with",
    }

    # Extract words
    words = re.findall(
        r"[a-zA-Z0-9]+",
        topic,
    )

    # Remove filler words
    words = [
        word
        for word in words
        if word not in filler_words
    ]

    return " ".join(words).strip()


def parse_query(query):

    if not isinstance(query, str) or not query.strip():

        raise ValueError(
            "Search query cannot be empty."
        )

    query = query.strip()

    # Detect intent
    intent = detect_intent(query)

    # Extract topic
    topic = extract_topic(
        query,
        intent,
    )

    # Fallback if topic extraction produces nothing
    if not topic:
        topic = query.strip()

    return {
        "original_query": query,
        "topic": topic,
        "intent": intent,
    }
