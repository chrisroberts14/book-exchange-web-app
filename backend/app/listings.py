"""Listings end points for the API."""

from fastapi import APIRouter


listings_router = APIRouter()


@listings_router.get("/")
async def get_all_listings():
    """
    Gets all listings in the database.

    :return:
    """
    return
