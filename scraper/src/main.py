from fetcher import fetch
from bs4 import BeautifulSoup


if __name__ == "__main__":
    html, status = fetch("https://books.toscrape.com/catalogue/page-1.html", "catalogue-page-1.html")
    print(f"status={status}, html={html[:200]}...")  # Print the first 200 characters of the HTML