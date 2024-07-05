"""Test listings endpoints."""


class TestListingsRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the books root endpoint."""

    route = "/listings"

    def test_listings_root(self, client):
        """Test the listings root endpoint."""
        response = client.get(self.route)
        assert response.status_code == 200
