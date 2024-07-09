"""Module to test the authentication of the API."""

import pytest
from fastapi.routing import APIRoute

from backend.app import app


def get_all_endpoints():
    """
    Get all endpoints.

    :return:
    """
    endpoints = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        path = route.path
        if hasattr(route, "methods"):
            methods = route.methods
            for method in methods:
                if method in [
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE",
                    "PATCH",
                ]:  # Include the HTTP methods you want to test
                    endpoints.append({"path": path, "method": method.lower()})
    return endpoints


class TestAuth:  # pylint: disable=too-few-public-methods
    """Test all endpoints return a 401 without authentication."""

    @pytest.mark.parametrize("endpoint", get_all_endpoints())
    def test_auth_endpoints(self, un_auth_client, endpoint):
        """
        Test all endpoints return a 401 without authentication.

        :param un_auth_client:
        :return:
        """
        response = un_auth_client.request(endpoint["method"], endpoint["path"])
        assert response.status_code == 401, response.json()
