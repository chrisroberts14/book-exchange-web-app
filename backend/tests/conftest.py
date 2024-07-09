"""Module containing fixtures for the tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, event
from sqlalchemy.orm import Session, sessionmaker

from backend.app.api.token import create_access_token, get_current_user
from backend.app.api_models import UserOut, BookOut, ListingOut
from backend.app.common import hash_password
from backend.app.core.config import settings
from backend.app.core.db import get_db, Base
from backend.app.db_models import UserDb, BookDb, ListingDb
from backend.app import app

settings.DATABASE_URL = "sqlite://"
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
    poolclass=StaticPool,
)


# Enable foreign key constraints on connection
def _enable_foreign_keys(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Use the event listener to apply the function on new connections
event.listen(engine, "connect", _enable_foreign_keys)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Override the get_db dependency.

    :return:
    """
    # pylint: disable=duplicate-code
    connection = engine.connect()
    session = Session(bind=connection)
    savepoint = connection.begin_nested()
    try:
        yield session
    finally:
        session.close()
        savepoint.rollback()


@pytest.fixture(scope="function")
def db() -> Session:  # pylint: disable=redefined-outer-name
    """
    Fixture for the database.

    :return:
    """
    for session in override_get_db():
        try:
            yield session
        finally:
            session.rollback()


@pytest.fixture(scope="function")
def current_user_override(sample_user):  # pylint: disable=redefined-outer-name
    """
    Override the get_current_user dependency.

    :param sample_user:
    :return:
    """

    def get_sample_user():
        yield sample_user

    app.dependency_overrides[get_current_user] = get_sample_user
    yield
    app.dependency_overrides[get_current_user] = get_current_user


@pytest.fixture(scope="session")
def client(auth_token) -> Generator[TestClient, None, None]:  # pylint: disable=redefined-outer-name
    """
    Fixture for the test client.

    :return:
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        test_client.headers.update({"Authorization": f"Bearer {auth_token}"})
        yield test_client


@pytest.fixture(scope="session")
def auth_token() -> str:
    """
    Fixture for the auth token.

    :return:
    """
    return create_access_token({"sub": "test_user"})


@pytest.fixture(scope="function")
def sample_user(db: Session) -> UserOut:  # pylint: disable=redefined-outer-name
    """
    Fixture for a sample user.

    :param db:
    :return:
    """
    return UserDb.create(
        db,
        UserDb(
            username="sample_user",
            email="test@test.com",
            hashed_password=hash_password("password"),
        ),
    )


@pytest.fixture(scope="function")
def sample_book(db: Session, sample_user: UserOut) -> BookOut:  # pylint: disable=redefined-outer-name
    """
    Fixture for a sample book.

    :param db:
    :param sample_user:
    :return:
    """
    return BookDb.create(
        db,
        BookDb(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            description="Test Description",
            owner=sample_user,
        ),
    )


@pytest.fixture(scope="function")
def sample_book_list(db: Session, sample_user: UserOut) -> list[BookOut]:  # pylint: disable=redefined-outer-name
    """
    Fixture for a list of sample books.

    :param db:
    :param sample_user:
    :return:
    """
    return [
        BookDb.create(
            db,
            BookDb(
                title=f"Test Book {i}",
                author=f"Test Author {i}",
                isbn=f"{i}",
                description=f"Test Description {i}",
                owner=sample_user,
            ),
        )
        for i in range(10)
    ]


@pytest.fixture(scope="function")
def sample_listing(
    db: Session,  # pylint: disable=redefined-outer-name
    sample_user: UserOut,  # pylint: disable=redefined-outer-name
    sample_book: BookOut,  # pylint: disable=redefined-outer-name
) -> ListingOut:
    """
    Fixture for a sample listing.

    :param db:
    :param sample_user:
    :param sample_book:
    :return:
    """
    return ListingDb.create(
        db,
        ListingDb(
            title="Test Listing",
            book=sample_book,
            seller=sample_user,
            price=10.0,
        ),
    )
