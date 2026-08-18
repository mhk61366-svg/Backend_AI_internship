from fetcher import fetch
from extractor import get_book_links, get_book_record, get_next_page_url
from bs4 import BeautifulSoup
from models import BookRecord, convert_price_to_float
import json
import os
import time as time_module
from datetime import datetime, timezone

start_time = time_module.time()
run_start_iso = datetime.now(timezone.utc).isoformat()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")

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
    # unique_links.append("https://books.toscrape.com/catalogue/this-book-does-not-exist/index.html")
    failed_pages = []
    records = []
    for i, book_url in enumerate(unique_links, start=1):
        cache_key = f"book-{i:02d}.html"
        try:
            book_html, status = fetch(book_url, cache_key)
            if status != 200:
                failed_pages.append({"url": book_url, "status": status})
                continue
            record = get_book_record(book_html, book_url, page_url)
            records.append(record)
        except Exception as e:
            failed_pages.append({"url": book_url, "status": "error", "detail": str(e)})
            continue

    valid_records = []
    error_records = []
    seen_urls = set()

    for raw in records:
        if raw["product_url"] in seen_urls:
            continue
        seen_urls.add(raw["product_url"])

        try:
            price_gbp = convert_price_to_float(raw["price_text"])
            book = BookRecord(**raw, price_gbp=price_gbp)
            valid_records.append(book.model_dump())
        except Exception as e:
            error_records.append({"record": raw, "reason": str(e)})

    with open(os.path.join(OUTPUT_DIR, "books.json"), "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "errors.json"), "w", encoding="utf-8") as f:
        json.dump(error_records, f, indent=2)

    print(f"valid={len(valid_records)} errors={len(error_records)}")

    duration = round(time_module.time() - start_time, 2)

    cache_hits = sum(1 for _ in os.listdir(CACHE_DIR))  # rough proxy, fine for this scope

    run_report = {
        "start_time": run_start_iso,
        "duration_seconds": duration,
        "pages_fetched": len(records) + len(failed_pages),
        "valid_records": len(valid_records),
        "invalid_records": len(error_records),
        "failed_pages": len(failed_pages),
        "failed_page_details": failed_pages,
    }
    with open(os.path.join(OUTPUT_DIR, "run-report.json"), "w", encoding="utf-8") as f:
        json.dump(run_report, f, indent=2)

    print(run_report)