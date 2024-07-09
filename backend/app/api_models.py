"""Module defining api schemas."""

from uuid import UUID
from datetime import date

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model to define config."""

    model_config = ConfigDict(
        from_attributes=True,
    )


class Token(BaseModel):
    """Token model."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model."""

    username: str | None = None


class UserIn(BaseModel):
    """UserIn is a Pydantic model that represents the input data for creating a new user."""

    username: str
    email: str


class UserInPassword(UserIn):
    """Model that represents the input data for creating a new user with a password."""

    password: str


class UserPatch(BaseModel):
    """Used for update operations on users."""

    username: str | None = None
    email: str | None = None


class UserOut(UserIn):
    """UserOut is a Pydantic model that represents the output data for creating a new user."""

    id: UUID


class UserInDb(UserOut):
    """User as it is stored in the database."""

    hashed_password: str


class BookPatch(BaseModel):
    """Used for update operations on books."""

    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    description: str | None = None


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


class ListingBase(BaseModel):
    """Base model for a book listing."""

    title: str
    buyer: UserOut | None = None
    description: str | None = None
    price: float
    sold: bool = False
    listed_date: str = str(date.today())


class ListingIn(ListingBase):
    """Model for creating a new listing."""

    seller_id: UUID
    book_id: UUID


class ListingPatch(ListingBase):
    """Model for updating a listing."""

    title: str | None = None
    book: BookOut | None = None
    seller: UserOut | None = None
    buyer: UserOut | None = None
    description: str | None = None
    price: float | None = None
    sold: bool | None = None
    listed_date: str | None = None


class ListingOut(ListingBase):
    """ListingIn is a Pydantic model that represents the input data for creating a new listing."""

    id: UUID
    seller: UserOut
    book: BookOut
    buyer: UserOut | None
