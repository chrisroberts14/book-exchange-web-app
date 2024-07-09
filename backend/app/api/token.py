"""Module for logging in and getting a token."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from backend.app.api_models import UserOut
from backend.app.common import hash_password
from backend.app.core.db import get_db
from backend.app.db_models import UserDb

token = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/token")


@token.get("/test_auth/")
async def test_auth(tkn: str = Depends(oauth2_scheme)):
    """
    Test endpoint for authentication.

    :param tkn:
    :return:
    """
    return {"token": tkn}


@token.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Get a token.

    :param form_data:
    :param db:
    :return:
    """
    user = UserDb.get_user_by_username(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )
    hashed_password = hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}


def fake_decode_token(db: Session, tkn: str):
    """
    Decode token stub.

    TODO: Replace with real decode using JWT
    :param db:
    :param tkn:
    :return:
    """
    return UserDb.get_user_by_username(db, tkn)


async def get_current_user(
    tkn: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """
    Get current user.

    :param tkn:
    :param db:
    :return:
    """
    user = fake_decode_token(db, tkn)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@token.get("/me", response_model=UserOut)
async def get_me(
    current_user: Annotated[UserOut, Depends(get_current_user)],
) -> UserOut:
    """
    Get the current user.

    :return:
    """
    return current_user
