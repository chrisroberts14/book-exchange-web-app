"""Module containing fixtures for the tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

from backend.app.api_models import UserOut
from backend.app.core.config import settings
from backend.app.core.db import init_db, get_db
from backend.app import app
from backend.app.db_models import UserDb

settings.DATABASE_URL = "sqlite://"
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Override the get_db dependency.

    :return:
    """
    connection = engine.connect()
    transaction = connection.begin()
    with SessionLocal(bind=connection) as session:
        init_db(engine)
        yield session
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def db() -> Session:  # pylint: disable=redefined-outer-name
    """
    Fixture for the database.

    :return:
    """
    return next(override_get_db())


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
def user_sample(db) -> UserOut:  # pylint: disable=redefined-outer-name
    """
    Fixture for a sample user.

    :return:
    """
    user = UserDb(username="test", email="test@test.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
