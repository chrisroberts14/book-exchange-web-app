"""Module for book endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from backend.app.api_models import BookOut, BookIn, BookPatch
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


@books.get("/{book_id}")
async def get_book(book_id: UUID, db: Session = Depends(get_db)) -> BookOut:
    """
    Get a book by id.

    :param book_id: id of the book
    :param db: database session
    :return:
    """
    book = BookDb.get_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@books.patch("/{book_id}")
async def update_book(
    book_id: UUID, book_patch: BookPatch, db: Session = Depends(get_db)
) -> BookOut:
    """
    Update a book.

    :param book_id:
    :param book_patch:
    :param db:
    :return:
    """
    book = BookDb.get_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
    return BookDb.update(db, book_patch, book_id)


@books.delete("/{book_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: Session = Depends(get_db)) -> None:
    """
    Delete a book.

    :param book_id:
    :param db:
    :return:
    """
    book = BookDb.get_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
    BookDb.delete(db, book_id)
