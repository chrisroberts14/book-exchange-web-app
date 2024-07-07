"""Users end points for the API."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api_schemas import UserOut
from backend.db_models import UserDb, get_db

user_router = APIRouter()


@user_router.get("/")
async def get_all_users(db: Session = Depends(get_db)) -> list[UserOut]:
    """
    Gets all users in the database.

    :return:
    """
    return UserDb.get_all(db)
