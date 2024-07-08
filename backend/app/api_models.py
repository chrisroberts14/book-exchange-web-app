"""Module defining api schemas."""

from uuid import UUID

from pydantic import BaseModel


class UserIn(BaseModel):
    """UserIn is a Pydantic model that represents the input data for creating a new user."""

    username: str
    email: str


class UserOut(UserIn):
    """UserOut is a Pydantic model that represents the output data for creating a new user."""

    id: UUID
