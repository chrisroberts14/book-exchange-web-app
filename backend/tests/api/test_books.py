"""Test books endpoints."""


class TestBooksRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the books root endpoint."""

    route = "/books"

    def test_get_all_books(self, client, book):
        """
        Test the books root endpoint.

        :param client: Test client
        """
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        result = response.json()
        assert len(result) == 1
        assert result[0]["title"] == book.title
        assert result[0]["author"] == book.author
        assert result[0]["publication_date"] == book.publication_date
        assert result[0]["isbn"] == book.isbn
