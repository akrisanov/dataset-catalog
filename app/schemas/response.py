from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """A base Pydantic schema of the application."""

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1


class Message(BaseSchema):
    """Payload message of any kind of information or generic errors."""

    detail: str


class Paginator(BaseModel):
    """
    Pagination fields inside the payload:
    * total_count: total number of records
    * page: current requested page
    * max_per_page: max number of items of the requested collection
    """

    total_count: int
    page: int
    max_per_page: int


EMPTY_RESPONSE = {"content": None}


def error_response(description: str) -> dict:
    """Build a payload model with a specific description."""
    return {
        "model": Message,
        "description": description,
    }


def paginator_params(page: Optional[int] = 1, max_per_page: Optional[int] = 10) -> dict:
    """Build an object out of pagination params."""
    return {"page": page, "max_per_page": max_per_page}


def page_data(total_count: int, paginator: dict) -> dict:
    """Build a payload object out of paginator data."""
    return {
        "total_count": total_count,
        "page": paginator["page"],
        "max_per_page": paginator["max_per_page"],
    }
