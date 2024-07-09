"""Module containing database models and crud operations."""

from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.db import Base


class Crud:  # pylint: disable=too-few-public-methods
    """Base class for CRUD operations."""

    id = None

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

    @classmethod
    def get_all(cls, db):
        """
        Get all objects.

        :param db: database session
        :return: all objects
        """
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db, id_):
        """
        Get an object by id.

        :param db: database session
        :param id_: id of the object
        :return: object
        """
        return db.get(cls, id_)

    @classmethod
    def update(cls, db, obj, id_):
        """
        Update an object.

        :param db:
        :param obj:
        :param id_:
        :return:
        """
        db_obj = db.query(cls).filter(cls.id == id_).first()
        if db_obj is None:
            return None  # or raise an exception

        for key, value in obj.model_dump().items():
            if value is not None:
                setattr(db_obj, key, value)

        db.commit()
        return db.get(cls, id_)


class UserDb(Base, Crud):  # pylint: disable=too-few-public-methods
    """User database table."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str]
    email: Mapped[str]
    books: Mapped[list["BookDb"]] = relationship("BookDb", back_populates="owner")


class BookDb(Base, Crud):  # pylint: disable=too-few-public-methods
    """Book database table."""

    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    author: Mapped[str]
    isbn: Mapped[str]
    description: Mapped[str]
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserDb"] = relationship("UserDb", back_populates="books")
