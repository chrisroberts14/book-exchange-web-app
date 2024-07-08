"""Module to test books endpoints."""

from uuid import UUID, uuid4

from backend.app.api_models import BookIn
from backend.app.db_models import BookDb


class TestRoot:
    """Test the "/" endpoint."""

    route = "/books/"

    def test_create_book(self, client):
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
            owner_id=UUID("00000000-0000-0000-0000-000000000000"),
        )
        response = client.post(
            self.route,
            json=book.model_dump(mode="json"),
        )
        assert response.status_code == 201, response.json()
        # Check the response data
        book = BookIn(**response.json())
        assert book.title == book.title
        assert book.author == book.author
        assert book.isbn == book.isbn
        assert book.description == book.description
        assert book.owner_id == book.owner_id

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


class TestBookId:
    """Test the "/books/{book_id}" endpoint."""

    route = "/books/{book_id}"

    def test_get_by_id(self, client, db):
        """
        Test get book by id.

        :param client:
        :param db:
        :return:
        """
        # Create a book then get the book by id and check the response
        book = BookDb(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            description="Test Description",
            owner_id=UUID("00000000-0000-0000-0000-000000000000"),
        )
        book = BookDb.create(db, book)
        response = client.get(self.route.format(book_id=book.id))
        assert response.status_code == 200, response.json()
        assert response.json()["title"] == book.title
        assert response.json()["author"] == book.author
        assert response.json()["isbn"] == book.isbn
        assert response.json()["description"] == book.description
        assert UUID(response.json()["owner_id"]) == book.owner_id

    def test_get_by_id_not_found(self, client):
        """
        Test get book by id not found.

        :param client:
        :return:
        """
        response = client.get(self.route.format(book_id=uuid4()))
        assert response.status_code == 404, response.json()
