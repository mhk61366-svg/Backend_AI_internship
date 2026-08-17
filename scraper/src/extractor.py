from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime, timezone

BASE_URL = "https://books.toscrape.com/catalogue/"

def get_book_links(html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for article in soup.select("article.product_pod"):
        a_tag = article.select_one("h3 a")
        if a_tag and a_tag.get("href"):
            links.append(urljoin(page_url, a_tag["href"]))
    return links

def get_next_page_url(html: str, page_url: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    next_link = soup.select_one("li.next a")
    if next_link and next_link.get("href"):
        return urljoin(page_url, next_link["href"])
    return None

def get_book_record(html:str, product_url:str, source_page:str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    product = soup.select_one("div.product_main")

    title = product.select_one("h1").get_text(strip=True)

    price_text = product.select_one("p.price_color").get_text(strip=True)

    availability_text = product.select_one("p.availability").get_text(strip=True)

    rating_tag = product.select_one("p.star-rating")
    rating_classes = rating_tag.get("class", [])
    rating_text = next((c for c in rating_classes if c != "star-rating"), None)

    desc_tag = soup.select_one("#product_description")
    if desc_tag:
        desc_p = desc_tag.find_next_sibling("p")
        description = desc_p.get_text(strip=True) if desc_p else None
    else:
        description = None

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }