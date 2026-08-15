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