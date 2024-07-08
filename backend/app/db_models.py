"""Module containing database models and crud operations."""

from uuid import uuid4, UUID

from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.db import Base


class Crud:  # pylint: disable=too-few-public-methods
    """Base class for CRUD operations."""

    @classmethod
    def create(cls, db, obj):
        """
        Create a new object.

        :param obj: object to create
        :param db: database session
        :return: created object
        """
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


class UserDb(Base, Crud):  # pylint: disable=too-few-public-methods
    """User database table."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str]
    email: Mapped[str]
