"""Test books endpoints."""


class TestBooksRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the books root endpoint."""

    route = "/books"

    def test_books_root(self, client):
        """Test the books root endpoint."""
        response = client.get(self.route)
        assert response.status_code == 200
