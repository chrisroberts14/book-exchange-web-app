"""Module for listings endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from backend.app.api_models import ListingIn, ListingOut
from backend.app.core.db import get_db
from backend.app.db_models import ListingDb

listings = APIRouter()


@listings.get("/", response_model=list[ListingOut])
async def get_listings(db: Session = Depends(get_db)) -> list[ListingOut]:
    """
    Get all listings.

    :return:
    """
    return ListingDb.get_all(db)


@listings.post("/", status_code=HTTP_201_CREATED)
async def create_listing(data: ListingIn, db: Session = Depends(get_db)) -> ListingOut:
    """
    Create a listing.

    :return:
    """
    return ListingDb.create(db, ListingDb(**data.dict()))
