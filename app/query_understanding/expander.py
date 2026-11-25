
def expand_query(parsed_query):

    topic = parsed_query["topic"]
    intent = parsed_query["intent"]

    if not topic:
        return []

    # Generic search variations for different intentions
    intent_templates = {

        "concepts": [
            "{} fundamentals",
            "{} principles",
            "{} key concepts",
            "{} important topics"
        ],

        "comparison": [
            "{} comparison",
            "{} differences",
            "{} similarities"
        ],

        "advantages": [
            "{} benefits",
            "{} advantages",
            "{} applications"
        ],

        "disadvantages": [
            "{} limitations",
            "{} challenges",
            "{} disadvantages"
        ],

        "explanation": [
            "{} explanation",
            "{} how it works",
            "{} fundamentals"
        ],

        "types": [
            "{} types",
            "{} categories",
            "{} classification"
        ],

        "latest": [
            "{} recent developments",
            "{} current trends",
            "{} latest research"
        ],

        "general": [
            "{} overview",
            "{} introduction",
            "{} fundamentals"
        ]
    }

    templates = intent_templates.get(
        intent,
        intent_templates["general"]
    )

    expanded_queries = [topic]

    for template in templates:
        expanded_queries.append(
            template.format(topic)
        )

    # Remove duplicate queries
    return list(dict.fromkeys(expanded_queries))

def expand_query(parsed_query):

    topic = parsed_query["topic"]
    intent = parsed_query["intent"]

    if not topic:
        return []

    intent_templates = {

        "concepts": [
            "{} fundamentals",
            "{} principles",
            "{} key concepts",
            "{} important topics"
        ],

        "comparison": [
            "{} comparison",
            "{} differences",
            "{} similarities"
        ],

        "advantages": [
            "{} benefits",
            "{} advantages",
            "{} applications"
        ],

        "disadvantages": [
            "{} limitations",
            "{} challenges",
            "{} disadvantages"
        ],

        "explanation": [
            "{} explanation",
            "{} how it works",
            "{} fundamentals"
        ],

        "types": [
            "{} types",
            "{} categories",
            "{} classification"
        ],

        "latest": [
            "{} recent developments",
            "{} current trends",
            "{} latest research"
        ],

        "general": [
            "{} overview",
            "{} introduction",
            "{} fundamentals"
        ]
    }

    templates = intent_templates.get(
        intent,
        intent_templates["general"]
    )

    expanded_queries = [topic]

    for template in templates:

        expanded_queries.append(
            template.format(topic)
        )

    # Remove duplicates
    return list(dict.fromkeys(expanded_queries))
