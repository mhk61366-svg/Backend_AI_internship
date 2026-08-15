import os
import requests
import time

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/mhk61366-svg/Backend_AI_internship)"
TIMEOUT = 10
DELAY = 0.5  # seconds, only applies to real requests, never to cache reads
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")

def _cache_path(cache_key: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, cache_key)

def fetch(url: str, cache_key: str) -> tuple[str, int]:
    path = _cache_path(cache_key)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT  {cache_key}  size={len(html)}")
        return html, 200

    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    print(f"FETCH      {url}  status={response.status_code}  size={len(response.text)}")

    if response.status_code != 200:
        return "", response.status_code

    with open(path, "w", encoding="utf-8") as f:
        f.write(response.text)

    time.sleep(DELAY)  # politeness delay — only after a real network request
    return response.text, 200