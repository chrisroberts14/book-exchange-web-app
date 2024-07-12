"""Module for testing the user endpoints."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from backend.app.api_models import UserOut, BookOut, UserPatch, UserInPassword
from backend.app.db_models import UserDb


class TestUserRoot:  # pylint: disable=too-few-public-methods
    """Test the user root endpoint."""

    route = "/users/"

    def test_create_user(self, client: TestClient):
        """
        Test create user.

        :return:
        """
        user = UserInPassword(
            username="test", email="test@test.com", password="password"
        )
        response = client.post(self.route, json=user.model_dump())
        assert response.status_code == 201, response.json()

    def test_get_all_users(self, client: TestClient, db: Session):
        """
        Test get all users.

        :return:
        """
        # Create ten users then get all users and check the response
        users = [
            UserDb(
                username=f"test{i}", email=f"test{i}@test.com", hashed_password="test"
            )
            for i in range(10)
        ]
        db.bulk_save_objects(users)
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        assert {user.username for user in users} == {
            user["username"]
            for user in response.json()
            if "test_user" not in user["username"]
        }
        assert {user.email for user in users} == {
            user["email"]
            for user in response.json()
            if "test_user" not in user["username"]
        }


class TestUserById:
    """Test the "/users/{user_id}" endpoint."""

    route = "/users/{user_id}"

    def test_get_by_id(self, client: TestClient, sample_user: UserOut):
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

    def test_get_by_id_not_found(self, client: TestClient):
        """
        Test get user by id not found.

        :param client:
        :return:
        """
        response = client.get(self.route.format(user_id=uuid4()))
        assert response.status_code == 404, response.json()

    @pytest.mark.parametrize(
        "change",
        [
            {"username": "new_username"},
            {"email": "new@test.com"},
        ],
        ids=["change username", "change email"],
    )
    def test_update_user(
        self,
        client: TestClient,
        sample_user: UserOut,
        change: dict,
        current_user_override,  # pylint: disable=unused-argument
    ):
        """
        Test update user.

        :param client:
        :param sample_user:
        :return:
        """
        response = client.patch(
            self.route.format(user_id=sample_user.id),
            json=UserPatch(**change).model_dump(),
        )
        assert response.status_code == 200, response.json()
        result = UserOut(**response.json())
        assert result.id == sample_user.id
        assert getattr(result, list(change.keys())[0]) == list(change.values())[0]

    def test_update_user_bad(self, client: TestClient, current_user_override):  # pylint: disable=unused-argument
        """
        Test attempting to update a user that doesn't exist raises a 404.

        :param client:
        :return:
        """
        response = client.patch(
            self.route.format(user_id=uuid4()),
            json=UserPatch(username="new_username").model_dump(),
        )
        assert response.status_code == HTTP_404_NOT_FOUND, response.json()

    def test_update_user_not_logged_in(
        self, client: TestClient, db: Session, current_user_override
    ):  # pylint: disable=unused-argument
        """
        Test attempting to update a user without being logged in raises a 403.

        :param client:
        :param db:
        :param current_user_override:
        :return:
        """
        # Create a second user
        user = UserDb.create(
            db,
            UserDb(
                username="test2",
                email="test@test.com",
                hashed_password="test",
            ),
        )
        response = client.patch(
            self.route.format(user_id=user.id),
            json=UserPatch(username="new_username").model_dump(),
        )
        assert response.status_code == HTTP_403_FORBIDDEN, response.json()

    def test_user_delete(self, client: TestClient, sample_user: UserOut):
        """
        Test deleting a user works.

        :return:
        """
        response = client.delete(self.route.format(user_id=sample_user.id))
        assert response.status_code == 204, response.json()

    def test_user_delete_bad(self, client: TestClient):
        """
        Test attempting to delete a user that doesn't exist raises a 404.

        :param client:
        :return:
        """
        response = client.delete(self.route.format(user_id=uuid4()))
        assert response.status_code == 404, response.json()


class TestUserBooks:
    """Tests to test the "/users/{user_id}/books" endpoint."""

    def test_get_users_books(
        self, client: TestClient, sample_user: UserOut, sample_book: BookOut
    ):
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

    def test_get_users_books_not_found(self, client: TestClient):
        """
        Test get user's books not found.

        :param client:
        :return:
        """
        response = client.get(f"/users/{uuid4()}/books")
        assert response.status_code == 404, response.json()
