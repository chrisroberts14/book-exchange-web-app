"""Module to test listings endpoints."""

from starlette.status import HTTP_201_CREATED

from backend.app.api_models import ListingOut
from backend.app.db_models import ListingDb


class TestRoot:
    """Test the "/listings/" endpoint."""

    route = "/listings/"

    def test_create_listing(self, client, sample_book, sample_user):
        """
        Test creating a listing.

        :param client:
        :param sample_book:
        :param sample_user:
        :return:
        """
        data = {
            "title": "Test Listing",
            "book_id": str(sample_book.id),
            "seller_id": str(sample_user.id),
            "price": 10.0,
        }
        response = client.post(self.route, json=data)
        assert response.status_code == HTTP_201_CREATED, response.json()
        result = ListingOut(**response.json())
        assert result.title == data["title"]
        assert result.book.id == sample_book.id
        assert result.seller.id == sample_user.id

    def test_get_all_listings(self, client, db, sample_book_list, sample_user):
        """
        Test get all listings.

        :param client:
        :param sample_book_list:
        :param sample_user:
        :return:
        """
        listings = [
            ListingDb.create(
                db,
                ListingDb(
                    title=f"Test Listing {i}",
                    book=book,
                    seller=sample_user,
                    price=10.0,
                ),
            )
            for i, book in enumerate(sample_book_list)
        ]
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        assert len(response.json()) == len(listings)
        assert {listing.title for listing in listings} == {
            listing["title"] for listing in response.json()
        }
