"""Test users endpoints."""


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
