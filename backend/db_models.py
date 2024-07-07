"""Database models for the api."""

from uuid import UUID, uuid4

from sqlalchemy import create_engine, event, ForeignKey
from sqlalchemy import UUID as uuid_type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
)

from backend.config import Settings

DATABASE_URL = Settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute("pragma foreign_keys=ON")


event.listen(engine, "connect", _fk_pragma_on_connect)

Base = declarative_base()


def get_db():
    """Get a database session."""
    with SessionLocal() as db:
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()


class DBCrud:
    """Base class for database CRUD operations."""

    @classmethod
    def get_all(cls, db):
        """
        Geta all instances from the db.

        :param db:
        :return:
        """
        return db.query(cls).all()

    @classmethod
    def get_by_pk(cls, db, pk):
        """
        Get an instance by primary key.

        :param db:
        :param pk:
        :return:
        """
        return db.query(cls).get(pk)


class UserDb(Base, DBCrud):  # pylint: disable=too-few-public-methods
    """Database model for users."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str]
    email: Mapped[str]
    listings: Mapped[list["ListingDb"]] = relationship(
        "ListingDb", back_populates="seller", foreign_keys="ListingDb.seller_id"
    )
    purchases: Mapped[list["ListingDb"]] = relationship(
        "ListingDb", back_populates="buyer", foreign_keys="ListingDb.buyer_id"
    )


class BookDb(Base, DBCrud):  # pylint: disable=too-few-public-methods
    """Database model for books."""

    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    author: Mapped[str]
    publication_date: Mapped[str]
    isbn: Mapped[str]
    listing: Mapped["ListingDb"] = relationship("ListingDb", back_populates="book")


class ListingDb(Base, DBCrud):  # pylint: disable=too-few-public-methods
    """Database model for listings."""

    __tablename__ = "listings"

    seller_id: Mapped[UUID] = mapped_column(
        uuid_type, ForeignKey("users.id"), nullable=False
    )
    buyer_id: Mapped[UUID] = mapped_column(
        uuid_type, ForeignKey("users.id"), nullable=False
    )
    book_id: Mapped[UUID] = mapped_column(
        uuid_type, ForeignKey("books.id"), nullable=False
    )

    book: Mapped["BookDb"] = relationship("BookDb", back_populates="listing")
    seller: Mapped["UserDb"] = relationship(
        "UserDb", back_populates="listings", foreign_keys=[seller_id]
    )
    buyer: Mapped["UserDb"] = relationship(
        "UserDb", back_populates="purchases", foreign_keys=[buyer_id]
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    price: Mapped[float]
    condition: Mapped[str]
    sold: Mapped[bool]
    sold_price: Mapped[float]
    sold_date: Mapped[str]
    created_date: Mapped[str]
    updated_date: Mapped[str]
