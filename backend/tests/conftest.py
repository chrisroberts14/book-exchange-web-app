"""Module containing fixtures for the tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import settings
from backend.app.core.db import get_db, Base
from backend.app import app

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
    connection.begin()
    with SessionLocal(bind=connection) as session:
        Base.metadata.create_all(bind=engine)
        yield session
        Base.metadata.drop_all(bind=engine)


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
