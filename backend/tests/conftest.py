"""Module containing fixtures for the tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.db import init_db, get_db
from backend.app import app


def override_get_db():
    """
    Override the get_db dependency.

    :return:
    """
    settings.DATABASE_URL = "sqlite://"
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True,
        poolclass=StaticPool,
    )
    with Session(engine) as session:
        init_db(engine)
        yield session
        session.rollback()


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:  # pylint: disable=redefined-outer-name
    """
    Fixture for the database.

    :return:
    """
    settings.DATABASE_URL = "sqlite://"
    engine = create_engine(settings.DATABASE_URL)
    with Session(engine) as session:
        init_db(engine)
        yield session
        session.rollback()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:  # pylint: disable=redefined-outer-name
    """
    Fixture for the test client.

    :param db:
    :return:
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
