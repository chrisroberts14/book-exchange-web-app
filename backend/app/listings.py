"""Listings end points for the API."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api_schemas import ListingOut
from backend.db_models import ListingDb, get_db

listings_router = APIRouter()


@listings_router.get("/")
async def get_all_listings(db: Session = Depends(get_db)) -> list[ListingOut]:
    """
    Gets all listings in the database.

    :return:
    """
    return ListingDb.get_all(db)
