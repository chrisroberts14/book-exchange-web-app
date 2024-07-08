"""Module for book endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from backend.app.api_models import BookOut, BookIn
from backend.app.core.db import get_db
from backend.app.db_models import BookDb

books = APIRouter()


@books.post("/", status_code=HTTP_201_CREATED)
async def create_book(book: BookIn, db: Session = Depends(get_db)) -> BookOut:
    """
    Create a book.

    :param db:
    :param book: book to create
    :return:
    """
    db_book = BookDb(**book.dict())
    return BookDb.create(db, db_book)


@books.get("/")
async def get_all_books(db: Session = Depends(get_db)) -> list[BookOut]:
    """
    Get all books.

    :return:
    """
    return BookDb.get_all(db)
