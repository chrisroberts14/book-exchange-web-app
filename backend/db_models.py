"""Database models for the api."""

from uuid import UUID, uuid4

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

from backend.config import Settings

DATABASE_URL = Settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()


class UsersDb(Base):  # pylint: disable=too-few-public-methods
    """Database model for users."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str]
    email: Mapped[str]
