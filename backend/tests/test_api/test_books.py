"""Module to test books endpoints."""

from uuid import UUID

from backend.app.api_models import BookIn
from backend.app.db_models import BookDb, UserDb


class TestRoot:
    """Test the "/" endpoint."""

    route = "/books/"

    def test_create_book(self, client, db):
        """
        Test create book.

        :param client:
        :param db:
        :return:
        """
        user = UserDb(username="sample_user", email="test@test.com")
        db.add(user)
        db.flush()
        db.refresh(user)
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890",
            "description": "Test Description",
            "owner_id": str(user.id),
        }
        response = client.post(
            self.route,
            json=data,
        )
        assert response.status_code == 201, response.json()
        # Check the response data
        book = BookIn(**response.json())
        assert book.title == data["title"]
        assert book.author == data["author"]
        assert book.isbn == data["isbn"]
        assert book.description == data["description"]
        assert book.owner_id == UUID(data["owner_id"])

    def test_get_all_books(self, client, db):
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
                owner_id=UUID("00000000-0000-0000-0000-000000000000"),
            )
            for i in range(10)
        ]
        db.bulk_save_objects(books)
        response = client.get(self.route)
        assert response.status_code == 200, response.json()
        assert {book.title for book in books} == {
            book["title"] for book in response.json()
        }
