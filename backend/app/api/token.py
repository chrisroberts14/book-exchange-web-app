"""Module for logging in and getting a token."""

from datetime import timedelta, datetime
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from backend.app.api_models import UserOut, TokenData, Token
from backend.app.common import pwd_context
from backend.app.core.config import settings
from backend.app.core.db import get_db
from backend.app.db_models import UserDb

token = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/token")


def verify_password(plain_password: str, hashed_password: str):
    """
    Verify a password.

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> UserDb | bool:
    """
    Authenticate a user.

    :param db:
    :param username:
    :param password:
    :return
    """
    user = UserDb.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user(db: Session, username: str):
    """
    Get a user by username.

    :param db:
    :param username:
    :return
    """
    return UserDb.get_user_by_username(db, username)


async def get_current_user(
    tkn: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """
    Get current user.

    :param tkn:
    :param db:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(tkn, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
):
    """
    Create an access token.

    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


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
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@token.get("/me", response_model=UserOut)
async def get_me(
    current_user: Annotated[UserOut, Depends(get_current_user)],
) -> UserOut:
    """
    Get the current user.

    :return:
    """
    return current_user
