from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class RawRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: str
    fetched_at: str


class BookRecord(BaseModel):
    """The clean, validated shape stored in output/books.json"""

    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: str
    fetched_at: str

    @field_validator("product_url")
    @classmethod
    def must_be_https(cls, v):
        if not str(v).startswith("https://"):
            raise ValueError("product_url must be absolute https URL")
        return v
