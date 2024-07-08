"""Tests for the root endpoint."""


class TestRoot:  # pylint: disable=too-few-public-methods
    """Test the "/" endpoint."""

    def test_docs_redirect(self, client):
        """
        Test the docs redirect.

        :param client:
        :return:
        """
        response = client.get("/")
        assert response.status_code == 200, response.json()
        assert "/docs" in str(response.url)
