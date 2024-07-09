"""Module to test db functions."""

import pytest

from backend.app.api_models import UserOut, UserPatch
from backend.app.db_models import UserDb


class TestUserDb:
    """Test the userdb table."""

    def test_create_user(self, db):
        """
        Test create user.

        :param db:
        :return:
        """
        user = UserDb.create(db, UserDb(username="sample_user", email="test@test.com"))
        db_user = db.get(UserDb, user.id)
        assert db_user.username == user.username
        assert db_user.email == user.email

    def test_get_all_users(self, db):
        """
        Test get all users.

        :param db:
        :return:
        """
        users = [
            UserDb(username=f"Test User {i}", email=f"test{i}@test.com")
            for i in range(10)
        ]
        db.bulk_save_objects(users)
        db_users = UserDb.get_all(db)
        assert len(db_users) == 10
        assert {db_user.username for db_user in db_users} == {
            user.username for user in users
        }
        assert {db_user.email for db_user in db_users} == {user.email for user in users}

    def test_get_by_id(self, db, sample_user: UserOut):
        """
        Test get by id.

        :param db:
        :return:
        """
        db_user = UserDb.get_by_id(db, sample_user.id)
        assert db_user.id == sample_user.id

    @pytest.mark.parametrize(
        "change",
        [
            {"username": "new_username"},
            {"email": "test2@test.com"},
        ],
    )
    def test_update_user(self, db, sample_user: UserOut, change: dict):
        """
        Test update user.

        :param db:
        :param sample_user:
        :return:
        """
        patch = UserPatch(**change)
        updated_user = UserDb.update(
            db, UserPatch(**patch.model_dump()), sample_user.id
        )
        assert updated_user.id == sample_user.id
        assert getattr(updated_user, list(change.keys())[0]) == list(change.values())[0]
