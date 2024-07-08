"""Test users endpoints."""

from backend.app.api_schemas import UserIn
from backend.db_models import UserDb


class TestUsersRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the books root endpoint."""

    route = "/users"

    def test_get_all_users(self, client, user):
        """
        Test the users root endpoint.

        :param client: Test client
        """
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        result = response.json()
        assert len(result) == 1
        assert result[0]["username"] == user.username
        assert result[0]["email"] == user.email

    def test_create_user(self, client, db):
        """
        Tests the create user endpoint.

        :param client:
        :return:
        """
        data = UserIn(username="test", email="test@test.com")
        response = client.post(self.route, json=data.dict())
        assert response.status_code == 201, response.json()
        result = response.json()
        assert result["username"] == data.username
        assert result["email"] == data.email
        # Check the user is actually in the database
        db_user = UserDb.get_by_id(db, result["id"])
        assert db_user.username == data.username
        assert db_user.email == data.email
