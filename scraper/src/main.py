from fetcher import fetch
from extractor import get_book_links, get_next_page_url
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
    print(f"catalogue_pages={min(page_number, 3)} discovered={all_book_links} unique_urls={len(unique_links)}")