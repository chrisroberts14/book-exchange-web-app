"""Common methods used in the app."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hash a password.

    :param password:
    :return:
    """
    return pwd_context.hash(password)
