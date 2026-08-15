"""
Stage 1: Fetch once, cache once.

Every real request:
- sends an honest User-Agent
- has a timeout
- checks the status code before doing anything else
- is saved to cache/ so re-running the script during development
  never hits the site again for the same URL
"""
import hashlib
import time
from pathlib import Path

import requests

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/AnujUpadhayay07/scraper)"
TIMEOUT_SECONDS = 10
MIN_DELAY_SECONDS = 0.5
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"

CACHE_DIR.mkdir(exist_ok=True)

_last_request_time = 0.0


def _cache_path(url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"{digest}.html"


def _polite_delay():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < MIN_DELAY_SECONDS:
        time.sleep(MIN_DELAY_SECONDS - elapsed)
    _last_request_time = time.time()


def fetch(url: str, retries: int = 1) -> tuple[str | None, str]:
    """
    Returns (html, outcome) where outcome is one of:
    "cache", "fetch", "not_found", "forbidden", "failed"

    Retries once on timeout / 5xx. Never retries 404 or 403.
    """
    cache_file = _cache_path(url)
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8"), "cache"

    attempt = 0
    while True:
        attempt += 1
        _polite_delay()
        try:
            response = requests.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS
            )
        except requests.RequestException:
            if attempt <= retries:
                time.sleep(1.5 * attempt)
                continue
            return None, "failed"

        if response.status_code == 200:
            cache_file.write_text(response.text, encoding="utf-8")
            return response.text, "fetch"
        if response.status_code == 404:
            return None, "not_found"
        if response.status_code == 403:
            return None, "forbidden"
        if 500 <= response.status_code < 600 and attempt <= retries:
            time.sleep(1.5 * attempt)
            continue
        return None, "failed"


def print_fetch_summary(url: str, html: str | None, outcome: str):
    size = len(html) if html else 0
    label = "CACHE HIT" if outcome == "cache" else outcome.upper()
    print(f"[{label}] {url} ({size} bytes)")
