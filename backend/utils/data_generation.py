"""
Generates a bunch of data into the database for testing purposes.

The data is random strings not real data.
"""

import random

from sqlalchemy.orm import Session

from backend.app.core.db import engine
from backend.app.db_models import UserDb, BookDb, ListingDb


def generate_random_string(length: int = 10):
    """
    Generate a random string.

    :return:
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choices(alphabet, k=length))


def generate_random_email():
    """
    Generate a random email.

    :return:
    """
    return generate_random_string() + "@example.com"


def main():
    """
    Begin the data generation process.

    :return:
    """
    # Get a database session.
    connection = engine.connect()
    db = Session(bind=connection)

    # Generate users
    users = [
        UserDb(
            username=generate_random_string(),
            email=generate_random_email(),
            hashed_password=generate_random_string(),
        )
        for _ in range(10)
    ]
    db.bulk_save_objects(users)
    db.commit()
    users = UserDb.get_all(db)
    user_ids = [user.id for user in users]

    # Generate books
    books = [
        BookDb(
            title=generate_random_string(),
            author=generate_random_string(),
            isbn=generate_random_string(),
            description=generate_random_string(),
            owner_id=random.choice(user_ids),
        )
        for _ in range(10)
    ]
    db.bulk_save_objects(books)
    db.commit()
    books = BookDb.get_all(db)

    # Generate listings
    books_in_listings = random.choices(books, k=10)
    books_sellers = [(book.owner_id, book.id) for book in books_in_listings]
    listings = [
        ListingDb(
            title=generate_random_string(),
            price=random.randint(1, 100),
            book_id=book_sellar[1],
            seller_id=book_sellar[0],
        )
        for book_sellar in books_sellers
    ]
    db.bulk_save_objects(listings)
    db.commit()
    connection.commit()


if __name__ == "__main__":
    main()
