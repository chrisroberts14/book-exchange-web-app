"""Module for listings endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from backend.app.api_models import ListingIn, ListingOut, ListingPatch
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


@listings.get("/{listing_id}", response_model=ListingOut)
async def get_listing(listing_id: UUID, db: Session = Depends(get_db)) -> ListingOut:
    """
    Get a listing by id.

    :param listing_id: id of the listing
    :param db: database session
    :return:
    """
    listing = ListingDb.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing


@listings.patch("/{listing_id}")
async def update_listing(
    listing_id: UUID, data: ListingPatch, db: Session = Depends(get_db)
) -> ListingOut:
    """
    Update a listing.

    :return:
    """
    listing = ListingDb.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Listing not found")
    return ListingDb.update(db, data, listing_id)
