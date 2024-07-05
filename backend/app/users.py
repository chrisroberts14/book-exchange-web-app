"""Users end points for the API."""

from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/")
async def get_all_users():
    """
    Gets all users in the database.

    :return:
    """
    return
