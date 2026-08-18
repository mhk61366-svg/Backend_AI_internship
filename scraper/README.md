## Target Classification

**Site:** [books.toscrape.com](https://books.toscrape.com)

**Why this target is appropriate:** Books to Scrape is a practice sandbox built
specifically for people to learn web scraping on. It is not a real bookstore —
no real products, no real transactions, no real company behind it. The site's
own "About" page states it exists for this exact purpose.

**Scope:** Only the first 3 catalogue pages (60 books total). No other pages,
sections, or endpoints on this site are accessed.

**Data collected per book:** title, product URL, price, availability text,
star rating, description, source catalogue page, and fetch timestamp.

**robots.txt check:** Requested `https://books.toscrape.com/robots.txt` once.
The request returned a 404 — no robots.txt file exists on this site. A missing
file is not the same as explicit permission, so permission here is instead
based on the site's own stated purpose as a public scraping sandbox, not on
the robots file.

I will not reuse this code on another site without checking its rules and
terms first.

## How to Run

```powershell
git clone https://github.com/mhk61366-svg/Backend_AI_internship/
cd Backend_AI_internship/scraper
python -m venv venv        # or use your existing api_env
venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd src
python main.py
```
Output lands in `../output/books.json`, `../output/errors.json`, and `../output/run-report.json`.

---

## Lane & Install

**Lane:** Python 3.10+
**Dependencies** (`requirements.txt`):
- `requests` — HTTP fetching
- `beautifulsoup4` + `lxml` — HTML parsing
- `pydantic` — record schema validation

Install with `pip install -r requirements.txt` inside an active virtual environment.

---

## Record Schema

Each validated record in `books.json` follows this shape (`models.py`, `BookRecord`):

| Field | Type | Notes |
|---|---|---|
| `title` | string | |
| `product_url` | string | absolute URL, must start with `https://` — this is the record's identity/canonical key |
| `price_text` | string | raw price as shown on the page, e.g. `"£51.77"` |
| `price_gbp` | float | numeric price, e.g. `51.77` |
| `availability_text` | string | raw stock text, e.g. `"In stock (22 available)"` |
| `rating_text` | string \| null | word-form rating as shown on site, e.g. `"Three"` |
| `description` | string \| null | `null` when the book page has no description — never invented |
| `source_page` | string | absolute URL of the catalogue page the book was discovered on |
| `fetched_at` | string | ISO 8601 UTC timestamp of when the detail page was fetched |

Records that fail validation are written to `errors.json` with a `reason` field instead of being silently dropped.

---

## Politeness Rules Followed

- Every real request sends an identifying `User-Agent`: `FlyRankInternshipA9/1.0 https://github.com/mhk61366-svg/Backend_AI_internship/
- 10-second timeout on every request — no request waits indefinitely
- 0.5-second delay between real (non-cached) requests
- Status code is checked before any parsing happens; only `200` is treated as success
- All pages (catalogue + detail) are cached to `cache/` on first fetch; reruns during development read from cache instead of re-hitting the live site
- Retries once on `5xx`/timeout errors only; `404`/`403` are never retried

---

## Known Limitation
`cache_hits` in `run-report.json` is a rough proxy — it counts the total
number of files currently in `cache/`, not a true per-run count of how many
requests were served from cache vs. fetched live during that specific run.
For a rerun where everything is cached, this is accurate; but it doesn't
distinguish "cached from this run" vs. "cached from a previous run" if the
cache folder already had files in it beforehand.
---

## Sample Run Report
```json
{
  "start_time": "2026-08-18T05:34:20.697571+00:00",
  "duration_seconds": 1.83,
  "pages_fetched": 60,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0,
  "failed_page_details": []
}
```

---

## Why No Browser Was Needed
Books to Scrape serves all book data directly inside the server-rendered HTML — nothing is loaded afterward via JavaScript. Since the data we need is already present in the raw response, fetching with `requests` and parsing with BeautifulSoup is sufficient; a headless browser like Playwright would only add startup cost and complexity with no benefit for this specific site.

---

## Ethics Note
This scraper only targets Books to Scrape, a site explicitly built and maintained for scraping practice — not a real business. Where an official API exists for a target, that should be used instead of scraping. This code does not bypass logins, paywalls, or any access blocks, and only collects the fields needed for the assignment. It is not intended for reuse against any other site without first checking that site's own rules and terms.