"""Users end points for the API."""

from fastapi import APIRouter

from backend.app.api_schemas import User

user_router = APIRouter()


@user_router.get("/")
async def get_all_users() -> list[User]:
    """
    Gets all users in the database.

    :return:
    """
    return [User(username="johndoe", email="test@test.com")]
