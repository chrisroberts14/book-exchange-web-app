"""Module containing database models and crud operations."""

from datetime import date
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

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

    @classmethod
    def delete(cls, db, id_):
        """
        Delete an object.

        :param db: database session
        :param id_: id of the object
        :return: None
        """
        db_obj = db.get(cls, id_)
        db.delete(db_obj)
        db.commit()


class UserDb(Base, Crud):  # pylint: disable=too-few-public-methods
    """User database table."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    books: Mapped[list["BookDb"]] = relationship(
        "BookDb", back_populates="owner", cascade="all, delete"
    )
    listings: Mapped[list["ListingDb"]] = relationship(
        "ListingDb",
        back_populates="seller",
        foreign_keys="ListingDb.seller_id",
        cascade="all, delete",
    )
    purchases: Mapped[list["ListingDb"]] = relationship(
        "ListingDb",
        back_populates="buyer",
        foreign_keys="ListingDb.buyer_id",
        cascade="all, delete",
    )

    @classmethod
    def get_user_by_username(cls, db: Session, username: str):
        """
        Get user by username.

        :return:
        """
        return db.query(cls).filter_by(username=username).first()


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
        "ListingDb", back_populates="book", uselist=False, cascade="all, delete"
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
