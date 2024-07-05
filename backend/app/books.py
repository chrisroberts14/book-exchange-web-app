"""Book end points for the API."""

from fastapi import APIRouter


book_router = APIRouter()


@book_router.get("/")
async def get_all_books():
    """
    Gets all books in the database.

    :return:
    """
    return
