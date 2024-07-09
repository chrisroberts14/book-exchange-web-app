"""Module to test db functions."""

from datetime import timedelta, date

import pytest
from sqlalchemy.orm import Session

from backend.app.api_models import (
    UserOut,
    UserPatch,
    BookPatch,
    ListingPatch,
    BookOut,
    ListingOut,
)
from backend.app.db_models import UserDb, BookDb, ListingDb


class TestUserDb:
    """Test the userdb table."""

    def test_create_user(self, db: Session):
        """
        Test create user.

        :param db:
        :return:
        """
        user = UserDb.create(
            db,
            UserDb(
                username="sample_user", email="test@test.com", hashed_password="test"
            ),
        )
        db_user = db.get(UserDb, user.id)
        assert db_user.username == user.username
        assert db_user.email == user.email

    def test_get_all_users(self, db: Session):
        """
        Test get all users.

        :param db:
        :return:
        """
        users = [
            UserDb(
                username=f"Test User {i}",
                email=f"test{i}@test.com",
                hashed_password="test",
            )
            for i in range(10)
        ]
        db.bulk_save_objects(users)
        db_users = UserDb.get_all(db)
        assert len(db_users) == 10
        assert {db_user.username for db_user in db_users} == {
            user.username for user in users
        }
        assert {db_user.email for db_user in db_users} == {user.email for user in users}

    def test_get_by_id(self, db: Session, sample_user: UserOut):
        """
        Test get by id.

        :param db:
        :return:
        """
        db_user = UserDb.get_by_id(db, sample_user.id)
        assert db_user.id == sample_user.id

    @pytest.mark.parametrize(
        "change",
        [
            {"username": "new_username"},
            {"email": "test2@test.com"},
        ],
    )
    def test_update_user(self, db: Session, sample_user: UserOut, change: dict):
        """
        Test update user.

        :param db:
        :param sample_user:
        :return:
        """
        updated_user = UserDb.update(db, UserPatch(**change), sample_user.id)
        assert updated_user.id == sample_user.id
        assert getattr(updated_user, list(change.keys())[0]) == list(change.values())[0]

    def test_delete_user(self, db: Session, sample_user: UserOut):
        """
        Test delete user.

        :param db:
        :param sample_user:
        :return:
        """
        UserDb.delete(db, sample_user.id)
        assert UserDb.get_by_id(db, sample_user.id) is None

    def test_delete_user_cascade(
        self, db: Session, sample_user: UserOut, sample_listing: ListingOut
    ):
        """
        Test delete user cascade deletes both owned books and listings.

        .
        :param db:
        :param sample_user:
        :param sample_listing:
        :return:
        """
        UserDb.delete(db, sample_user.id)
        assert UserDb.get_by_id(db, sample_user.id) is None
        assert BookDb.get_by_id(db, sample_listing.book_id) is None
        assert ListingDb.get_by_id(db, sample_listing.id) is None


class TestBookDb:
    """Class to test the book table."""

    def test_create_book(self, db: Session, sample_user: UserOut):
        """
        Test creating a book.

        :param db:
        :return:
        """
        book = BookDb(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            description="Test Description",
            owner_id=sample_user.id,
        )
        db_book = BookDb.create(db, book)
        assert db_book.title == book.title
        assert db_book.owner.id == book.owner_id

    def test_get_all_books(self, db: Session, sample_user: UserOut):
        """
        Test getting all books.

        :param db:
        :param sample_user:
        :return:
        """
        books = [
            BookDb(
                title=f"Test Book {i}",
                author=f"Test Author {i}",
                isbn=f"1234567890 {i}",
                description=f"Test Description {i}",
                owner_id=sample_user.id,
            )
            for i in range(10)
        ]
        db.bulk_save_objects(books)
        db_books = BookDb.get_all(db)
        assert all(
            db_book.title in [book.title for book in books] for db_book in db_books
        )
        assert all(db_book.owner.id == sample_user.id for db_book in db_books)

    def test_get_book_by_id(self, db: Session, sample_book: BookOut):
        """
        Test getting a book by id.

        :param db:
        :param sample_book:
        :return:
        """
        db_book = BookDb.get_by_id(db, sample_book.id)
        assert db_book.id == sample_book.id
        assert db_book.title == sample_book.title
        assert db_book.owner.id == sample_book.owner.id

    @pytest.mark.parametrize(
        "change",
        [
            {"title": "New Title"},
            {"author": "New Author"},
            {"isbn": "1234567890"},
            {"description": "New Description"},
        ],
        ids=["title", "author", "isbn", "description"],
    )
    def test_update_book(self, db: Session, sample_book: BookOut, change: dict):
        """
        Test updating a book.

        :param db:
        :param sample_book:
        :return:
        """
        updated_user = BookDb.update(db, BookPatch(**change), sample_book.id)
        assert updated_user.id == sample_book.id
        assert getattr(updated_user, list(change.keys())[0]) == list(change.values())[0]

    def test_delete_book(self, db: Session, sample_book: BookOut):
        """
        Test delete book.

        :param db:
        :param sample_book:
        :return:
        """
        BookDb.delete(db, sample_book.id)
        assert BookDb.get_by_id(db, sample_book.id) is None

    def test_delete_book_cascade(
        self, db: Session, sample_book: BookOut, sample_listing: ListingOut
    ):
        """
        Test delete book cascade deletes listings.

        .
        :param db:
        :param sample_book:
        :param sample_listing:
        :return:
        """
        BookDb.delete(db, sample_book.id)
        assert BookDb.get_by_id(db, sample_listing.book_id) is None
        assert ListingDb.get_by_id(db, sample_listing.id) is None


class TestListingDb:
    """Class to test the listing table."""

    def test_create(self, db: Session, sample_user: UserOut, sample_book: BookOut):
        """
        Test create a listing.

        :return:
        """
        listing = ListingDb(
            title="Test Listing",
            book=sample_book,
            seller=sample_user,
            price=10.0,
        )
        db_listing = ListingDb.create(db, listing)
        assert db_listing.title == listing.title
        assert db_listing.seller.id == listing.seller_id
        assert db_listing.book.id == listing.book_id

    def test_get_all(
        self, db: Session, sample_user: UserOut, sample_book_list: list[BookOut]
    ):
        """
        Test get all listings.

        :return:
        """
        listings = []
        for i, book in enumerate(sample_book_list):
            listing = ListingDb(
                title=f"Test Listing {i}",
                book=book,
                seller=sample_user,
                price=10.0,
            )
            listings.append(ListingDb.create(db, listing))
        db_listings = ListingDb.get_all(db)
        assert all(
            db_listing.title in [listing.title for listing in listings]
            for db_listing in db_listings
        )
        assert all(db_listing.seller.id == sample_user.id for db_listing in db_listings)
        assert all(
            db_listing.book.id in [book.id for book in sample_book_list]
            for db_listing in db_listings
        )

    def test_get_by_id(self, db: Session, sample_listing: ListingOut):
        """
        Test getting a listing by id.

        :return:
        """
        db_listing = ListingDb.get_by_id(db, sample_listing.id)
        assert db_listing.id == sample_listing.id

    @pytest.mark.parametrize(
        "change",
        [
            {"title": "New Title"},
            {"price": 20.0},
            {"description": "New Description"},
            {"sold": True},
            {"listed_date": str(date.today() - timedelta(days=1))},
        ],
        ids=["title", "price", "description", "sold", "listed_date"],
    )
    def test_update(self, db: Session, sample_listing: ListingOut, change: dict):
        """
        Test update method.

        :param db:
        :param sample_listing:
        :param change:
        :return:
        """
        updated_listing = ListingDb.update(
            db, ListingPatch(**change), sample_listing.id
        )
        assert updated_listing.id == sample_listing.id
        assert (
            getattr(updated_listing, list(change.keys())[0]) == list(change.values())[0]
        )

    def test_delete_listing(self, db: Session, sample_listing: ListingOut):
        """
        Test delete listing.

        :param db:
        :param sample_listing:
        :return:
        """
        ListingDb.delete(db, sample_listing.id)
        assert ListingDb.get_by_id(db, sample_listing.id) is None
