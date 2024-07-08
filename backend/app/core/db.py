"""Module containing database functions."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session

from backend.app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
Base = declarative_base()


def init_db(db_engine=engine):  # pragma: no cover
    """
    Create the database.

    Alembic should actually be used, but you may want to use this method for testing
    :return:
    """
    Base.metadata.create_all(bind=db_engine)


def get_db() -> Generator[Session, None, None]:  # pragma: no cover
    """
    Gets a database session.

    :return:
    """
    connection = engine.connect()
    session = Session(bind=connection)
    savepoint = connection.begin_nested()
    try:
        yield session
    except SQLAlchemyError as e:
        savepoint.rollback()
        raise e
    finally:
        session.close()
