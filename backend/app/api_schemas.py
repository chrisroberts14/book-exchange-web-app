"""Module defining the schemas for the API."""

from datetime import date

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    A user in the api.

    This will have some authentication information at some point
    """

    username: str
    email: EmailStr


class Book(BaseModel):
    """A book in the api."""

    title: str
    author: str
    publication_date: date
    isbn: str


class Listing(BaseModel):
    """A listing in the api."""

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
