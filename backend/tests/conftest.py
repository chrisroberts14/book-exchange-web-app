"""Pytest fixtures."""

import pytest

from fastapi.testclient import TestClient
from backend.app import app


@pytest.fixture(scope="session")
def client():
    """
    Get the test client for the FastAPI app.

    :return: TestClient
    """
    return TestClient(app)
