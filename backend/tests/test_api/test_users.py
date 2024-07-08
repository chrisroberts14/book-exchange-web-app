"""Module for testing the user endpoints."""

from backend.app.api_models import UserIn
from backend.app.db_models import UserDb


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

    def test_get_all_users(self, client, db):
        """
        Test get all users.

        :return:
        """
        # Create ten users then get all users and check the response
        users = [
            UserDb(username=f"test{i}", email=f"test{i}@test.com") for i in range(10)
        ]
        db.bulk_save_objects(users)
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        assert {user.username for user in users} == {
            user["username"] for user in response.json()
        }
        assert {user.email for user in users} == {
            user["email"] for user in response.json()
        }
