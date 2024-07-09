"""Module for testing the user endpoints."""

from uuid import uuid4

from backend.app.api_models import UserIn, UserOut, BookOut
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


class TestUserById:
    """Test the "/users/{user_id}" endpoint."""

    route = "/users/{user_id}"

    def test_get_by_id(self, client, sample_user: UserOut):
        """
        Test get user by id.

        :param client:
        :param sample_user:
        :return:
        """
        response = client.get(self.route.format(user_id=sample_user.id))
        result = UserOut(**response.json())
        assert response.status_code == 200, response.json()
        assert result.id == sample_user.id

    def test_get_by_id_not_found(self, client):
        """
        Test get user by id not found.

        :param client:
        :return:
        """
        response = client.get(self.route.format(user_id=uuid4()))
        assert response.status_code == 404, response.json()


class TestUserBooks:
    """Tests to test the "/users/{user_id}/books" endpoint."""

    def test_get_users_books(self, client, sample_user: UserOut, sample_book: BookOut):
        """
        Test get user's books.

        :param client:
        :param sample_user:
        :return:
        """
        response = client.get(f"/users/{sample_user.id}/books")
        assert response.status_code == 200, response.json()
        for book_json in response.json():
            book = BookOut(**book_json)
            assert book.owner.id == sample_user.id
            assert book.id == sample_book.id

    def test_get_users_books_not_found(self, client):
        """
        Test get user's books not found.

        :param client:
        :return:
        """
        response = client.get(f"/users/{uuid4()}/books")
        assert response.status_code == 404, response.json()
