"""Book end points for the API."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api_schemas import BookOut
from backend.db_models import get_db, BookDb

book_router = APIRouter()


@book_router.get("/")
async def get_all_books(db: Session = Depends(get_db)) -> list[BookOut]:
    """
    Gets all books in the database.

    :return:
    """
    return BookDb.get_all(db)
