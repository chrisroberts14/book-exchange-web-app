"""Module defining the schemas for the API."""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    A user in the api.

    This will have some authentication information at some point
    """

    id: UUID
    username: str
    email: EmailStr


class Book(BaseModel):
    """A book in the api."""

    id: UUID
    title: str
    author: str
    publication_date: date
    isbn: str


class Listing(BaseModel):
    """A listing in the api."""

    id: UUID
    book: Book
    price: float
    condition: str
    seller: User
    sold: bool
    sold_to: User = None
    sold_price: float = None
    sold_date: date = None
    created_date: date
    updated_date: date
