"""
Test token endpoint.

This is the login endpoint
"""

from fastapi.testclient import TestClient

from backend.app.api_models import UserOut


class TestLogin:
    """Test the login at endpoint "/token/token"."""

    route = "/token/token"

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
        assert response.status_code == 400, response.json()

    def test_login_bad_password(self, client: TestClient, sample_user: UserOut):
        """
        Test login with a bad password.

        :return:
        """
        response = client.post(
            self.route,
            data={"username": sample_user.username, "password": "bad_password"},
        )
        assert response.status_code == 400, response.json()


class TestCurrentUser:  # pylint: disable=too-few-public-methods
    """Test get current user."""

    route = "/token/me"

    def test_get_current_user(self, client: TestClient, sample_user: UserOut):
        """
        Test get current user.

        :param client:
        :param sample_user:
        :return:
        """
        response = client.get(
            self.route, headers={"Authorization": f"Bearer {sample_user.username}"}
        )
        assert response.status_code == 200, response.json()
        assert response.json()["username"] == sample_user.username
