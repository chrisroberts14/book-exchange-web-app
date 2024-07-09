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


class UserPatch(BaseModel):
    """Used for update operations on users."""

    username: str | None = None
    email: str | None = None


class UserOut(UserIn):
    """UserOut is a Pydantic model that represents the output data for creating a new user."""

    id: UUID


class BookPatch(BaseModel):
    """Used for update operations on books."""

    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    description: str | None = None


class BookBase(BaseModel):
    """Base model for book types."""

    title: str | None
    author: str | None
    isbn: str | None
    description: str | None = "No description provided."


class BookIn(BookBase):
    """BookIn is a Pydantic model that represents the input data for creating a new book."""

    owner_id: UUID


class BookOut(BookBase):
    """BookOut is a Pydantic model that represents the output data for creating a new book."""

    id: UUID
    owner: UserOut
