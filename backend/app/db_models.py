"""Module containing database models and crud operations."""

from datetime import date
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.db import Base


class Crud:  # pylint: disable=too-few-public-methods
    """Base class for CRUD operations."""

    id = NotImplemented

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
    listings: Mapped[list["ListingDb"]] = relationship(
        "ListingDb", back_populates="seller", foreign_keys="ListingDb.seller_id"
    )
    purchases: Mapped[list["ListingDb"]] = relationship(
        "ListingDb", back_populates="buyer", foreign_keys="ListingDb.buyer_id"
    )


class BookDb(Base, Crud):  # pylint: disable=too-few-public-methods
    """Book database table."""

    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    author: Mapped[str]
    isbn: Mapped[str]
    description: Mapped[str]
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserDb"] = relationship(
        "UserDb", back_populates="books", foreign_keys=[owner_id]
    )
    listing: Mapped["ListingDb"] = relationship(
        "ListingDb", back_populates="book", uselist=False
    )


class ListingDb(Base, Crud):
    """Listing database table."""

    __tablename__ = "listings"

    book_id: Mapped[UUID] = mapped_column(ForeignKey("books.id"), unique=True)
    book: Mapped["BookDb"] = relationship(
        "BookDb", back_populates="listing", foreign_keys=[book_id]
    )
    seller_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    seller: Mapped["UserDb"] = relationship(
        "UserDb", back_populates="listings", foreign_keys=[seller_id]
    )
    buyer_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), default=None, nullable=True
    )
    buyer: Mapped["UserDb"] = relationship(
        "UserDb", back_populates="purchases", foreign_keys=[buyer_id]
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    price: Mapped[float]
    sold: Mapped[bool] = mapped_column(default=False)
    listed_date: Mapped[str] = mapped_column(default=str(date.today()))
