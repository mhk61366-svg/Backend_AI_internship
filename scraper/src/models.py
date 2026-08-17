from pydantic import BaseModel, field_validator
import re

class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str 
    rating_text: str | None
    description: str | None
    source_page: str
    fetched_at: str

    @field_validator("product_url","source_page")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError("URL must be absolute and start with https://")
        return v

def convert_price_to_float(price_text: str) -> float:
    cleaned = re.sub(r"[^\d.]", "", price_text)
    return float(cleaned)