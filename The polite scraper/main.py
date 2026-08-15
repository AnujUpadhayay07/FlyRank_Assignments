import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from extract import extract_book, find_book_links, find_next_page, normalize_price
from http_client import fetch, print_fetch_summary
from schema import BookRecord, RawRecord

BASE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Add a deliberately broken URL here to test Stage 5. Leave empty for a
# normal run, or add one fake entry, e.g.:
# EXTRA_TEST_URLS = ["https://books.toscrape.com/catalogue/does-not-exist/index.html"]
EXTRA_TEST_URLS: list[str] = []


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def discover_catalogue_pages() -> tuple[list, int]:
    pages = []
    cache_hits = 0
    url = BASE_CATALOGUE_URL
    while url and len(pages) < 3:
        html, outcome = fetch(url)
        print_fetch_summary(url, html, outcome)
        if outcome == "cache":
            cache_hits += 1
        if not html:
            break
        pages.append((url, html))
        url = find_next_page(html, url)
    return pages, cache_hits


def discover_book_links(catalogue_pages) -> list[str]:
    all_links = []
    for page_url, html in catalogue_pages:
        all_links.extend(find_book_links(html, page_url))
    seen = set()
    unique = []
    for link in all_links:
        if link not in seen:
            seen.add(link)
            unique.append(link)
    return unique


def run():
    start_time = time.time()
    fetched_pages = 0
    cache_hits = 0
    failed_pages = 0
    valid_records: list[dict] = []
    invalid_records: list[dict] = []

    catalogue_pages, cat_cache_hits = discover_catalogue_pages()
    cache_hits += cat_cache_hits
    fetched_pages += len(catalogue_pages)

    book_urls = discover_book_links(catalogue_pages)
    print(
        f"catalogue_pages={len(catalogue_pages)} "
        f"discovered={len(book_urls)} unique_urls={len(book_urls)}"
    )

    book_urls += EXTRA_TEST_URLS

    for book_url in book_urls:
        source_page = catalogue_pages[0][0] if catalogue_pages else ""
        html, outcome = fetch(book_url)
        print_fetch_summary(book_url, html, outcome)

        if outcome == "cache":
            cache_hits += 1
        elif outcome == "fetch":
            fetched_pages += 1

        if not html:
            failed_pages += 1
            invalid_records.append({"url": book_url, "reason": f"fetch failed: {outcome}"})
            continue

        try:
            raw = extract_book(html, book_url, source_page, now_iso())
            RawRecord(**raw)
        except Exception as e:
            failed_pages += 1
            invalid_records.append({"url": book_url, "reason": f"extract error: {e}"})
            continue

        price_gbp = normalize_price(raw["price_text"])
        candidate = {**raw, "price_gbp": price_gbp}

        try:
            record = BookRecord(**candidate)
            valid_records.append(json.loads(record.model_dump_json()))
        except ValidationError as e:
            invalid_records.append({"url": book_url, "reason": str(e)})

    deduped = {}
    for r in valid_records:
        deduped[r["product_url"]] = r
    valid_records = list(deduped.values())

    (OUTPUT_DIR / "books.json").write_text(json.dumps(valid_records, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "errors.json").write_text(json.dumps(invalid_records, indent=2), encoding="utf-8")

    report = {
        "start_time": datetime.fromtimestamp(start_time, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_seconds": round(time.time() - start_time, 2),
        "pages_fetched": fetched_pages,
        "cache_hits": cache_hits,
        "valid_records": len(valid_records),
        "invalid_records": len(invalid_records),
        "failed_pages": failed_pages,
    }
    (OUTPUT_DIR / "run-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n--- RUN REPORT ---")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
