"""Test module to test the root endpoint."""

from fastapi import status


class TestRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the root endpoint."""

    route = "/"

    def test_root(self, client):
        """
        Test the root endpoint.

        :param client: Test client
        """
        response = client.get(self.route)
        assert response.status_code is status.HTTP_200_OK
        assert "/docs" in str(response.url)
