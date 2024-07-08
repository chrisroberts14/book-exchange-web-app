"""Module to test db functions."""

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
