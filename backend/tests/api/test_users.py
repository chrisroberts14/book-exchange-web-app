"""Test users endpoints."""


class TestUsersRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the books root endpoint."""

    route = "/users"

    def test_users_root(self, client):
        """
        Test the users root endpoint.

        :param client: Test client
        """
        response = client.get(self.route)
        assert response.status_code == 200
