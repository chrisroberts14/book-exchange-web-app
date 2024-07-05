"""Listings end points for the API."""

from datetime import date

from fastapi import APIRouter

from backend.app.api_schemas import Listing, Book, User

listings_router = APIRouter()


@listings_router.get("/")
async def get_all_listings() -> list[Listing]:
    """
    Gets all listings in the database.

    :return:
    """
    return [
        Listing(
            book=Book(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                publication_date="1925-04-10",
                isbn="9780333791035",
            ),
            price=0.01,
            condition="new",
            seller=User(username="johndoe", email="test@test.com"),
            sold=False,
            sold_to=User(username="janedoe", email="test@test.com"),
            sold_price=0.02,
            sold_date=date.today(),
            created_date=date.today(),
            updated_date=date.today(),
        )
    ]
