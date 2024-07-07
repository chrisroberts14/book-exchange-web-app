"""Test listings endpoints."""


class TestListingsRoot:  # pylint: disable=too-few-public-methods
    """Test class to test the books root endpoint."""

    route = "/listings"

    def test_get_all_listings(self, client, listing):
        """
        Test the listings root endpoint.

        :param client: Test client
        """
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        result = response.json()
        assert len(result) == 1
        assert result[0]["book"]["title"] == listing.book.title
        assert result[0]["seller"]["username"] == listing.seller.username
        assert result[0]["buyer"]["username"] == listing.buyer.username
        assert result[0]["price"] == listing.price
        assert result[0]["condition"] == listing.condition
        assert result[0]["sold"] == listing.sold
        assert result[0]["id"] == str(listing.id)
        assert result[0]["book"]["id"] == str(listing.book_id)
        assert result[0]["seller"]["id"] == str(listing.seller_id)
        assert result[0]["buyer"]["id"] == str(listing.buyer_id)
