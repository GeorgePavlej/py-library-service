from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer


BOOK_URL = reverse("books:book-list")


def detail_url(book_id: int):
    return reverse("books:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "Test book",
        "author": "Test author",
        "cover": "Hardcover",
        "inventory": 5,
        "daily_fee": 1.00,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_unauthenticated_user_can_read_books(self) -> None:
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_create_book_forbidden(self) -> None:
        payload = {
            "title": "Test book",
            "author": "Test author",
            "cover": "Hardcover",
            "inventory": 5,
            "daily_fee": 1.00,
        }

        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_books_list(self) -> None:
        sample_book()
        sample_book(title="Another Test Book", author="Another Test Author")

        res = self.client.get(BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_single_book(self) -> None:
        book = sample_book()

        url = reverse("books:book-detail", args=[book.id])
        res = self.client.get(url)

        serializer = BookSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book(self) -> None:
        payload = {
            "title": "Test book",
            "author": "Test author",
            "cover": "Hardcover",
            "inventory": 5,
            "daily_fee": 1.00,
        }

        res = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_update_book_with_patch(self) -> None:
        book = sample_book()

        payload = {"title": "Updated Title", "author": "Updated Author"}
        self.client.patch(detail_url(book_id=book.id), payload)

        book.refresh_from_db()
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_update_book_with_put(self) -> None:
        book = sample_book()

        payload = {
            "title": "Updated Title",
            "author": "Updated Author",
            "cover": "Softcover",
            "inventory": 10,
            "daily_fee": 2.00,
        }

        self.client.put(detail_url(book_id=book.id), payload)

        book.refresh_from_db()
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_delete_book(self) -> None:
        book = sample_book()

        res = self.client.delete(detail_url(book_id=book.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

    def test_filter_books_by_title(self) -> None:
        book1 = sample_book(title="Test Book 1", author="Test Author")
        book2 = sample_book(title="Test Book 2", author="Another Test Author")
        sample_book(title="Unrelated Title", author="Unrelated Author")

        res = self.client.get(BOOK_URL, {"title": "Test Book"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]["id"], book1.id)
        self.assertEqual(res.data[1]["id"], book2.id)
