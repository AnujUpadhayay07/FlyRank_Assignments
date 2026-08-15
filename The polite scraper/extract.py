import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

RATING_WORDS = {"One", "Two", "Three", "Four", "Five"}


def find_book_links(catalogue_html: str, page_url: str) -> list[str]:
    """Absolute URLs to every book on a catalogue page."""
    soup = BeautifulSoup(catalogue_html, "html.parser")
    links = []
    for article in soup.select("article.product_pod h3 a"):
        href = article.get("href")
        if href:
            links.append(urljoin(page_url, href))
    return links


def find_next_page(catalogue_html: str, page_url: str) -> str | None:
    soup = BeautifulSoup(catalogue_html, "html.parser")
    next_link = soup.select_one("li.next a")
    if next_link and next_link.get("href"):
        return urljoin(page_url, next_link["href"])
    return None


def extract_book(detail_html: str, book_url: str, source_page: str, fetched_at: str) -> dict:
    """Pull the 8 raw fields from a single book detail page."""
    soup = BeautifulSoup(detail_html, "html.parser")
    product_main = soup.select_one("div.product_main")

    title = product_main.select_one("h1").get_text(strip=True)

    price_el = product_main.select_one("p.price_color")
    price_text = price_el.get_text(strip=True) if price_el else ""

    availability_el = product_main.select_one("p.availability")
    availability_text = (
        availability_el.get_text(strip=True) if availability_el else ""
    )

    rating_el = product_main.select_one("p.star-rating")
    rating_text = "Unknown"
    if rating_el:
        classes = rating_el.get("class", [])
        for c in classes:
            if c in RATING_WORDS:
                rating_text = c
                break

    desc_heading = soup.find("div", id="product_description")
    description = None
    if desc_heading:
        desc_p = desc_heading.find_next_sibling("p")
        if desc_p:
            description = desc_p.get_text(strip=True)

    return {
        "title": title,
        "product_url": book_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at,
    }


def normalize_price(price_text: str) -> float | None:
    """'£51.77' -> 51.77"""
    match = re.search(r"[\d.]+", price_text)
    if not match:
        return None
    try:
        return float(match.group())
    except ValueError:
        return None
