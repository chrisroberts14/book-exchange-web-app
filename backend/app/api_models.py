"""Module defining api schemas."""

from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model to define config."""

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserIn(BaseModel):
    """UserIn is a Pydantic model that represents the input data for creating a new user."""

    username: str
    email: str


class UserOut(UserIn):
    """UserOut is a Pydantic model that represents the output data for creating a new user."""

    id: UUID


class BookBase(BaseModel):
    """Base model for book types."""

    title: str
    author: str
    isbn: str
    description: str = "No description provided."


class BookIn(BookBase):
    """BookIn is a Pydantic model that represents the input data for creating a new book."""

    owner_id: UUID


class BookOut(BookBase):
    """BookOut is a Pydantic model that represents the output data for creating a new book."""

    id: UUID
    owner: UserOut
