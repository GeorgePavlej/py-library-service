from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment
from user.models import User


BORROWING_URL = reverse("borrowings:borrowing-list")


def create_test_user(email, password):
    return User.objects.create_user(email=email, password=password)


def create_test_book(title, author, inventory, daily_fee):
    return Book.objects.create(
        title=title, author=author, inventory=inventory, daily_fee=daily_fee
    )


def create_test_borrowing(user, book, borrow_date, expected_return_date):
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=borrow_date,
        expected_return_date=expected_return_date,
    )
    payment = Payment.objects.create(
        borrowing=borrowing,
        session_id="test_session_id",
        amount=10,
    )
    return borrowing


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class BorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_borrowing(self):
        user = create_test_user("test@example.com", "password")
        book = create_test_book("Test Book", "Test Author", 5, 10)

        self.client.force_authenticate(user=user)

        data = {
            "book": book.id,
            "borrow_date": date.today().strftime("%Y-%m-%d"),
            "expected_return_date": (
                    date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
        }

        response = self.client.post(
            reverse("borrowings:borrowing-list"), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Borrowing.objects.count(), 1)
        borrowing = Borrowing.objects.first()
        self.assertEqual(borrowing.user, user)
        self.assertEqual(borrowing.book, book)

    def test_list_borrowings(self):
        user = create_test_user("test@example.com", "password")
        book = create_test_book("Test Book", "Test Author", 5, 10)
        borrowing = create_test_borrowing(
            user,
            book,
            date.today(),
            date.today() + timedelta(days=5)
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("borrowings:borrowing-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], borrowing.id)
        self.assertEqual(response.data[0]["book"]["id"], book.id)
        self.assertEqual(
            response.data[0]["borrow_date"],
            borrowing.borrow_date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            response.data[0]["expected_return_date"],
            borrowing.expected_return_date.strftime("%Y-%m-%d")
        )

    def test_return_borrowing(self):
        user = create_test_user("test@example.com", "password")
        book = create_test_book("Test Book", "Test Author", 5, 10)
        borrowing = create_test_borrowing(
            user,
            book,
            date.today(),
            date.today() + timedelta(days=5)
        )

        payment = borrowing.payments.first()
        payment.status = payment.PaymentStatus.PAID
        payment.save()

        self.client.force_authenticate(user=user)

        response = self.client.post(reverse("borrowings:return-borrowing", args=[borrowing.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        borrowing.refresh_from_db()
        self.assertEqual(borrowing.actual_return_date, date.today())
