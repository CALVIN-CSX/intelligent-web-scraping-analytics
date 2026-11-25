
from app.search import search


def run_test(query, source="web"):

    print("=" * 80)
    print("INTELLIGENT WEB SEARCH TEST")
    print("=" * 80)

    print("\nQuery:", query)
    print("Source:", source)

    try:

        response = search(
            query=query,
            source=source,
            limit=10,
        )

        parsed_query = response.get(
            "parsed_query",
            {},
        )

        print("\n" + "-" * 80)
        print("QUERY UNDERSTANDING")
        print("-" * 80)

        print(
            "Topic:",
            parsed_query.get("topic"),
        )

        print(
            "Intent:",
            parsed_query.get("intent"),
        )

        print("\n" + "-" * 80)
        print("EXPANDED QUERIES")
        print("-" * 80)

        for expanded_query in response.get(
            "expanded_queries",
            [],
        ):

            print(
                "-",
                expanded_query,
            )

        print("\n" + "-" * 80)
        print("GENERATED ANSWER")
        print("-" * 80)

        print(
            response.get(
                "answer",
                "No answer generated.",
            )
        )

        print("\n" + "-" * 80)
        print("RETRIEVED ARTICLES")
        print("-" * 80)

        results = response.get(
            "results",
            [],
        )

        if not results:

            print(
                "No articles retrieved."
            )

        for index, article in enumerate(
            results,
            start=1,
        ):

            print(
                f"\nArticle {index}"
            )

            print(
                "Title:",
                article.get(
                    "title",
                    "Untitled",
                ),
            )

            print(
                "Source:",
                article.get(
                    "source",
                    "Unknown",
                ),
            )

            print(
                "URL:",
                article.get(
                    "url",
                    "",
                ),
            )

            print(
                "Relevance Score:",
                article.get(
                    "score",
                    "N/A",
                ),
            )

            print(
                "Word Count:",
                article.get(
                    "word_count",
                    "N/A",
                ),
            )

            print(
                "Keywords:",
                article.get(
                    "keywords",
                    [],
                ),
            )

        print("\n" + "=" * 80)
        print("TEST COMPLETED")
        print("=" * 80)

    except Exception as error:

        print("\nTEST FAILED")
        print("Error:", error)

        raise


if __name__ == "__main__":

    query = (
        "Advantages and disadvantages "
        "of renewable energy"
    )

    run_test(
        query,
        source="web",
    )
