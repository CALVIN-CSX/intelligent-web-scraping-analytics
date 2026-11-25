
from app.search import search

from app.answer_generation.generator import (
    collect_sentences,
    select_sentences,
)


QUERY = (
    "Advantages and disadvantages "
    "of renewable energy"
)


def run_debug():

    print("=" * 80)
    print("GENERATOR DEBUG TEST")
    print("=" * 80)

    response = search(
        query=QUERY,
        source="web",
        limit=10,
    )

    parsed_query = response.get(
        "parsed_query",
        {},
    )

    articles = response.get(
        "results",
        [],
    )

    topic = parsed_query.get(
        "topic",
        "the searched topic",
    )

    intent = parsed_query.get(
        "intent",
        "general",
    )

    print("\nQUERY:", QUERY)
    print("TOPIC:", topic)
    print("INTENT:", intent)

    print("\n" + "=" * 80)
    print("ARTICLE COUNT:", len(articles))
    print("=" * 80)

    # --------------------------------------------------
    # Collect candidate sentences
    # --------------------------------------------------

    candidates = collect_sentences(
        articles,
        topic,
    )

    print(
        "\nTOTAL CANDIDATE SENTENCES:",
        len(candidates),
    )

    # --------------------------------------------------
    # Display top candidates
    # --------------------------------------------------

    print("\n" + "=" * 80)
    print("TOP 30 CANDIDATE SENTENCES")
    print("=" * 80)

    for index, item in enumerate(
        candidates[:30],
        start=1,
    ):

        print(f"\n[{index}]")

        print(
            "Score:",
            round(
                item["score"],
                4,
            ),
        )

        print(
            "Classification:",
            item["classification"],
        )

        print(
            "Article:",
            item["article"].get(
                "title",
                "Untitled",
            ),
        )

        print(
            "Sentence:",
            item["sentence"],
        )

    # --------------------------------------------------
    # Balanced selection using detected intent
    # --------------------------------------------------

    selected = select_sentences(
        candidates,
        limit=12,
        intent=intent,
    )

    print("\n" + "=" * 80)
    print("SELECTED SENTENCES")
    print("=" * 80)

    for index, item in enumerate(
        selected,
        start=1,
    ):

        print(f"\n[{index}]")

        print(
            "Score:",
            round(
                item["score"],
                4,
            ),
        )

        print(
            "Classification:",
            item["classification"],
        )

        print(
            "Article:",
            item["article"].get(
                "title",
                "Untitled",
            ),
        )

        print(
            "Sentence:",
            item["sentence"],
        )

    # --------------------------------------------------
    # Classification summary
    # --------------------------------------------------

    advantage_count = sum(
        1
        for item in selected
        if item["classification"] == "advantages"
    )

    disadvantage_count = sum(
        1
        for item in selected
        if item["classification"] == "disadvantages"
    )

    neutral_count = sum(
        1
        for item in selected
        if item["classification"] == "neutral"
    )

    print("\n" + "=" * 80)
    print("SELECTION SUMMARY")
    print("=" * 80)

    print(
        "Advantages:",
        advantage_count,
    )

    print(
        "Disadvantages:",
        disadvantage_count,
    )

    print(
        "Neutral:",
        neutral_count,
    )

    print(
        "Total Selected:",
        len(selected),
    )

    print("\n" + "=" * 80)
    print("DEBUG TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    run_debug()
