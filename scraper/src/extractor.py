from urllib.parse import urljoin
from bs4 import BeautifulSoup

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