def display(normalized_data):
    if not normalized_data:
        print("No data found.")
        return

    for item in normalized_data:
        print(f"\nTitle: {item['title']}")
        print(f"Source: {item['source']}")
        print(f"ID: {item['id']}")
        print(f"URL: {item['url']}")

        if item["text"] is not None:
            print(f"Text: {item['text']}")

        if item["data"] is not None:
            print("Data:")
            print(item["data"])
