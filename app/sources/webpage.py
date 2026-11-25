
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def extract_webpage(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
        )

        response.raise_for_status()

        # Only process HTML pages
        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "text/html" not in content_type:
            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Remove unwanted elements
        for element in soup.select(
            "script, style, nav, footer, header, "
            "aside, form, noscript"
        ):
            element.decompose()

        # Try to find the main content
        main_content = (
            soup.find("main")
            or soup.find("article")
            or soup.body
        )

        if not main_content:
            return None

        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else ""
        )

        text = main_content.get_text(
            separator=" ",
            strip=True,
        )

        # Clean excessive whitespace
        text = " ".join(text.split())

        if not text:
            return None

        return {
            "title": title,
            "url": url,
            "text": text,
            "source": "webpage",
        }

    except Exception as error:

        print(f"Webpage extraction error: {error}")

        return None
