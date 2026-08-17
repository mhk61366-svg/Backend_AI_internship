from fetcher import fetch
from extractor import get_book_links, get_book_record, get_next_page_url
from bs4 import BeautifulSoup


if __name__ == "__main__":
    page_url = "https://books.toscrape.com/catalogue/page-1.html"
    all_book_links = []

    for page_number in range(1, 4):
        cache_key = f"catalogue-page-{page_number}.html"
        html, status_code = fetch(page_url, cache_key)

        if status_code != 200:
            print(f"Failed to fetch {page_url}, status code: {status_code}")
            break

        book_links = get_book_links(html, page_url)
        all_book_links.extend(book_links)

        next_page_url = get_next_page_url(html, page_url)
        if not next_page_url:
            print("No more pages found.")
            break

        page_url = next_page_url

    unique_links = list(dict.fromkeys(all_book_links))  # de-dupe, keep order
    records = []
    for i, book_url in enumerate(unique_links, start=1):
        cache_key = f"book-{i:02d}.html"
        book_html, status = fetch(book_url, cache_key)
        if status != 200:
            continue
        record = get_book_record(book_html, book_url, page_url)
        records.append(record)

    print(
        "First record:\n"
        + "=" * 60
        + "\n"
        + "\n".join(
            f"{key.replace('_', ' ').title()}: "
            + (
                " ".join(str(value).split()[:30]) + "..."
                if key.lower() == "description" and isinstance(value, str) and len(str(value).split()) > 30
                else str(value)
            )
            for key, value in records[0].items()
        )
        + "\n"
        + "=" * 60
    )
    print(f"detail_pages={len(records)}")