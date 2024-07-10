"""
Test token endpoint.

This is the login endpoint
"""

from datetime import timedelta

from fastapi.testclient import TestClient
from starlette.status import HTTP_401_UNAUTHORIZED

from backend.app.api_models import UserOut
from backend.app.api.auth import create_access_token


class TestLogin:
    """Test the login at endpoint "/auth/login"."""

    route = "/auth/login"

    def test_login_good(self, client: TestClient, sample_user: UserOut):
        """
        Test login.

        :return:
        """
        response = client.post(
            self.route, data={"username": sample_user.username, "password": "password"}
        )
        assert response.status_code == 200, response.json()

    def test_login_bad_username(self, client: TestClient):
        """
        Test login with a bad username.

        :return:
        """
        response = client.post(
            self.route, data={"username": "bad_username", "password": "password"}
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED, response.json()

    def test_login_bad_password(self, client: TestClient, sample_user: UserOut):
        """
        Test login with a bad password.

        :return:
        """
        response = client.post(
            self.route,
            data={"username": sample_user.username, "password": "bad_password"},
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED, response.json()


class TestCurrentUser:  # pylint: disable=too-few-public-methods
    """Test get current user."""

    route = "/auth/me"

    def test_get_current_user(self, client: TestClient, sample_user: UserOut):
        """
        Test get current user.

        :param client:
        :param sample_user:
        :return:
        """
        access_token_expires = timedelta(minutes=1)
        token = create_access_token(
            {"sub": sample_user.username}, expires_delta=access_token_expires
        )
        response = client.get(self.route, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, response.json()
        assert response.json()["username"] == sample_user.username

    def test_get_current_user_no_auth(self, client: TestClient):
        """
        Test get current user without authorization.

        :param client:
        :return:
        """
        response = client.get(self.route)
        assert response.status_code == HTTP_401_UNAUTHORIZED, response.json()

    def test_get_current_user_bad_auth(self, client: TestClient):
        """
        Test get current user with bad authorization.

        :param client:
        :return:
        """
        response = client.get(self.route, headers={"Authorization": "Bearer bad_token"})
        assert response.status_code == HTTP_401_UNAUTHORIZED, response.json()

    def test_get_current_user_bad_username(self, client: TestClient):
        """
        Test get current user with bad username.

        :param client:
        :return:
        """
        access_token_expires = timedelta(minutes=1)
        token = create_access_token(
            {"sub": "bad_username"}, expires_delta=access_token_expires
        )
        response = client.get(self.route, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == HTTP_401_UNAUTHORIZED, response.json()

    def test_get_current_user_no_username(self, client: TestClient):
        """
        Test get current user with bad username.

        :param client:
        :return:
        """
        access_token_expires = timedelta(minutes=1)
        token = create_access_token({"sub": None}, expires_delta=access_token_expires)
        response = client.get(self.route, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == HTTP_401_UNAUTHORIZED, response.json()
