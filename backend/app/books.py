"""Book end points for the API."""

from datetime import date
from uuid import uuid4

from fastapi import APIRouter
from backend.app.api_schemas import BookOut

book_router = APIRouter()


@book_router.get("/")
async def get_all_books() -> list[BookOut]:
    """
    Gets all books in the database.

    :return:
    """
    # Stubbed
    return [
        BookOut(
            id=uuid4(),
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            publication_date=date.today(),
            isbn="9780333791035",
        )
    ]
