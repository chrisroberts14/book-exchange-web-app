"""Module to test listings endpoints."""

from datetime import date, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from fastapi.testclient import TestClient

from backend.app.api_models import ListingOut, ListingPatch, BookOut, UserOut
from backend.app.db_models import ListingDb


class TestRoot:
    """Test the "/listings/" endpoint."""

    route = "/listings/"

    def test_create_listing(
        self, client: TestClient, sample_book: BookOut, sample_user: UserOut
    ):
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

    def test_get_all_listings(
        self,
        client: TestClient,
        db: Session,
        sample_book_list: list[BookOut],
        sample_user: UserOut,
    ):
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


class TestListingByID:
    """Test the "/listings/{listing_id}" endpoint."""

    route = "/listings/{listing_id}"

    def test_get_by_id(self, client: TestClient, sample_listing: ListingOut):
        """
        Test getting a single listing.

        :param client:
        :param sample_listing:
        :return:
        """
        response = client.get(self.route.format(listing_id=sample_listing.id))
        assert response.status_code == HTTP_200_OK, response.json()
        result = ListingOut(**response.json())
        assert result.id == sample_listing.id

    def test_get_bad_id(self, client: TestClient):
        """
        Test getting a listing with a bad id.

        :param client:
        :return:
        """
        response = client.get(self.route.format(listing_id=uuid4()))
        assert response.status_code == HTTP_404_NOT_FOUND, response.json()

    @pytest.mark.parametrize(
        "change",
        [
            {"title": "New Title"},
            {"price": 20.0},
            {"description": "New Description"},
            {"sold": True},
            {"listed_date": str(date.today() - timedelta(days=1))},
        ],
        ids=["title", "price", "description", "sold", "listed_date"],
    )
    def test_update(self, client: TestClient, sample_listing: ListingOut, change: dict):
        """
        Test update listing endpoint.

        :param client:
        :param sample_listing:
        :return:
        """
        response = client.patch(
            self.route.format(listing_id=sample_listing.id),
            json=ListingPatch(**change).model_dump(exclude_none=True),
        )
        assert response.status_code == HTTP_200_OK, response.json()
        for key, value in change.items():
            assert response.json()[key] == value

    def test_update_bad_id(self, client: TestClient):
        """
        Test updating a listing with a bad id.

        :param client:
        :return:
        """
        response = client.patch(
            self.route.format(listing_id=uuid4()),
            json=ListingPatch(title="New Title").model_dump(exclude_none=True),
        )
        assert response.status_code == HTTP_404_NOT_FOUND, response.json()
