"""Module containing fixtures for the tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, event
from sqlalchemy.orm import Session, sessionmaker

from backend.app.api_models import UserOut, BookOut
from backend.app.core.config import settings
from backend.app.core.db import get_db, Base
from backend.app.db_models import UserDb, BookDb
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


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:  # pylint: disable=redefined-outer-name
    """
    Fixture for the test client.

    :return:
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def sample_user(db) -> UserOut:  # pylint: disable=redefined-outer-name
    """
    Fixture for a sample user.

    :param db:
    :return:
    """
    return UserDb.create(db, UserDb(username="sample_user", email="test@test.com"))


@pytest.fixture(scope="function")
def sample_book(db, sample_user: UserOut) -> BookOut:  # pylint: disable=redefined-outer-name
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
