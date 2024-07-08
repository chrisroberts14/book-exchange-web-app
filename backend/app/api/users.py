"""Module for user endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from backend.app.db_models import UserDb
from backend.app.api_models import UserOut, UserIn
from backend.app.core.db import get_db


users = APIRouter()


@users.post("/", status_code=HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserIn, db: Session = Depends(get_db)) -> UserOut:
    """
    Get all users.

    :return:
    """
    db_user = UserDb(username=user.username, email=user.email)
    return UserDb.create(db, db_user)
