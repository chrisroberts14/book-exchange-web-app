"""Module defining api schemas."""

from uuid import UUID

from pydantic import BaseModel


class BookIn(BaseModel):
    """BookIn is a Pydantic model that represents the input data for creating a new book."""

    title: str
    author: str
    isbn: str
    description: str = "No description provided."
    owner_id: UUID


class BookOut(BookIn):
    """BookOut is a Pydantic model that represents the output data for creating a new book."""

    id: UUID


class UserIn(BaseModel):
    """UserIn is a Pydantic model that represents the input data for creating a new user."""

    username: str
    email: str


class UserOut(UserIn):
    """UserOut is a Pydantic model that represents the output data for creating a new user."""

    id: UUID
    books: list[BookOut]
