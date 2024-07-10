"""Module for user endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from backend.app.api.auth import get_current_user
from backend.app.db_models import UserDb
from backend.app.api_models import UserOut, BookOut, UserPatch, UserInPassword
from backend.app.core.db import get_db
from backend.app.common import hash_password


users = APIRouter()


@users.post("/", status_code=HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserInPassword, db: Session = Depends(get_db)) -> UserOut:
    """
    Get all users.

    :return:
    """
    db_user = UserDb(**user.model_dump(exclude={"password"}))
    db_user.hashed_password = hash_password(user.password)
    return UserDb.create(db, db_user)


@users.get("/", response_model=list[UserOut])
async def get_all_users(db: Session = Depends(get_db)) -> list[UserOut]:
    """
    Get all users.

    :return:
    """
    return UserDb.get_all(db)


@users.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, db: Session = Depends(get_db)) -> UserOut:
    """
    Get a user by id.

    :param user_id: id of the user
    :param db: database session
    :return:
    """
    db_user = UserDb.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@users.get("/{user_id}/books", response_model=list[BookOut])
async def get_users_books(
    user_id: UUID, db: Session = Depends(get_db)
) -> list[BookOut]:
    """
    Get all books for a user.

    :param user_id:
    :param db:
    :return:
    """
    user = UserDb.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user.books


@users.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID,
    user_patch: UserPatch,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
) -> UserOut:
    """
    Update a user in the database.

    :param current_user:
    :param user_id:
    :param user_patch:
    :param db:
    :return:
    """
    db_user = UserDb.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="User can only update their own account",
        )
    return UserDb.update(db, user_patch, user_id)


@users.delete("/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> None:
    """
    Delete a user from the database.

    :param user_id:
    :param db:
    :return
    """
    user = UserDb.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    UserDb.delete(db, user_id)
