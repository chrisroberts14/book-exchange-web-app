"""Module for testing the user endpoints."""

from backend.app.api_models import UserIn


class TestUserRoot:  # pylint: disable=too-few-public-methods
    """Test the user root endpoint."""

    route = "/users/"

    def test_create_user(self, client):
        """
        Test create user.

        :return:
        """
        user = UserIn(username="test", email="test@test.com")
        response = client.post(self.route, json=user.model_dump())
        assert response.status_code == 201, response.json()
