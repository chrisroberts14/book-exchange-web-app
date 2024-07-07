"""Module defining the schemas for the API."""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    """
    A user in the api.

    Used for creating users
    """

    username: str
    email: EmailStr


class UserOut(UserIn):
    """
    A user in the api.

    Used for returning users
    """

    id: UUID


class BookIn(BaseModel):
    """A book in the api."""

    title: str
    author: str
    publication_date: date
    isbn: str


class BookOut(BookIn):
    """A book in the api."""

    id: UUID


class ListingIn(BaseModel):
    """A listing in the api."""

    book: BookOut
    price: float
    condition: str
    seller: UserOut
    buyer: UserOut
    sold: bool
    sold_price: float = None
    sold_date: date = None
    created_date: date
    updated_date: date


class ListingOut(ListingIn):
    """A listing in the api."""

    id: UUID
