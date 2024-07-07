"""Pytest fixtures."""

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.config import Settings
from backend.db_models import Base, get_db, UserDb, BookDb, ListingDb

Settings.SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    Settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():  # pylint: disable=redefined-outer-name
    """
    Override the get_db dependency to use the test database.

    :return:
    """
    db_session = TestingSessionLocal()
    yield db_session
    db_session.rollback()


@pytest.fixture(scope="function")
def db():  # pylint: disable=redefined-outer-name
    """
    Get a database session.

    :return: Session
    """
    with TestingSessionLocal() as db_session:
        yield db_session
        db_session.rollback()


@pytest.fixture(scope="session")
def client():  # pylint: disable=redefined-outer-name
    """
    Get the test client for the FastAPI app.

    :return: TestClient
    """
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function")
def user(db):  # pylint: disable=redefined-outer-name
    """
    Test user for use in tests.

    :return:
    """
    user_entry = UserDb(username="User 1", email="test@test.com")
    db.add(user_entry)
    db.flush()
    return UserDb.get_all(db)[0]


@pytest.fixture(scope="function")
def book(db):  # pylint: disable=redefined-outer-name
    """
    Test book for use in tests.

    :return:
    """
    book_entry = BookDb(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        publication_date="1925-04-10",
        isbn="9780333791035",
    )
    db.add(book_entry)
    db.flush()
    return BookDb.get_all(db)[0]


@pytest.fixture(scope="function")
def listing(db, user, book):  # pylint: disable=redefined-outer-name
    """
    Test listing for use in tests.

    :return:
    """
    listing_entry = ListingDb(
        book_id=book.id,
        price=0.01,
        condition="new",
        seller_id=user.id,
        sold=False,
        buyer_id=user.id,
        sold_price=0.02,
        sold_date="2021-01-01",
        created_date="2021-01-01",
        updated_date="2021-01-01",
    )
    db.add(listing_entry)
    db.flush()
    return ListingDb.get_all(db)[0]
