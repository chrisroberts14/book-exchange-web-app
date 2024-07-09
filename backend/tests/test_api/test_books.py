"""Module to test books endpoints."""

from uuid import uuid4

import pytest

from backend.app.api_models import BookIn, UserOut, BookOut, BookPatch
from backend.app.db_models import BookDb


class TestRoot:
    """Test the "/" endpoint."""

    route = "/books/"

    def test_create_book(self, client, sample_user: UserOut):
        """
        Test create book.

        :param client:
        :return:
        """
        book = BookIn(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            description="Test Description",
            owner_id=sample_user.id,
        )
        response = client.post(
            self.route,
            json=book.model_dump(mode="json"),
        )
        assert response.status_code == 201, response.json()
        # Check the response data
        result = BookOut(**response.json())
        assert book.title == result.title
        assert result.owner.id == book.owner_id

    def test_get_all_books(self, client, db, sample_user):
        """
        Test get all books.

        :param client:
        :param db:
        :return:
        """
        # Create 10 books then get all books and check the response
        books = [
            BookDb(
                title=f"Test Book {i}",
                author=f"Test Author {i}",
                isbn=f"{i}",
                description=f"Test Description {i}",
                owner_id=sample_user.id,
            )
            for i in range(10)
        ]
        db.bulk_save_objects(books)
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        assert {book.title for book in books} == {
            book["title"] for book in response.json()
        }


class TestBookId:
    """Test the "/books/{book_id}" endpoint."""

    route = "/books/{book_id}"

    def test_get_by_id(self, client, sample_book: BookOut):
        """
        Test get book by id.

        :param client:
        :param db:
        :return:
        """
        response = client.get(self.route.format(book_id=sample_book.id))
        assert response.status_code == 200, response.json()
        result = BookOut(**response.json())
        assert result.id == sample_book.id
        assert result.owner.id == sample_book.owner.id

    def test_get_by_id_not_found(self, client):
        """
        Test get book by id not found.

        :param client:
        :return:
        """
        response = client.get(self.route.format(book_id=uuid4()))
        assert response.status_code == 404, response.json()

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
    def test_update_book(self, client, sample_book: BookOut, change):
        """
        Test a patch of a book.

        :param client:
        :return:
        """
        patch = BookPatch(**change)
        response = client.patch(
            self.route.format(book_id=sample_book.id),
            json=patch.model_dump(exclude_none=True),
        )
        assert response.status_code == 200, response.json()
        for key, value in change.items():
            assert response.json()[key] == value

    def test_update_bad_book(self, client):
        """
        Test attempting to update a bad book results in a 404.

        :param client:
        :return:
        """
        response = client.patch(
            self.route.format(book_id=uuid4()),
            json={"title": "New Title"},
        )
        assert response.status_code == 404, response.json()
