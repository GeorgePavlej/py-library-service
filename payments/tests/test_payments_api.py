from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from borrowings.tests.test_borrowing_api import create_test_book
from payments.models import Payment
from payments.serializers import PaymentSerializer
from borrowings.models import Borrowing
from user.models import User


class PaymentSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword"
        )
        book = create_test_book("Test Book", "Test Author", 5, 10)
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=book,
        )
        self.payment = Payment.objects.create(
            borrowing=self.borrowing,
            amount=10.00
        )

    def test_payment_serialization(self):
        serializer = PaymentSerializer(self.payment)
        expected_data = {
            "id": self.payment.id,
            "status": Payment.PaymentStatus.PENDING,
            "payment_type": Payment.PaymentType.PAYMENT,
            "borrowing": self.borrowing.id,
            "amount": "10.00",
            "session_url": None,
        }

        self.assertEqual(serializer.data, expected_data)


class PaymentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword"
        )
        book = create_test_book("Test Book", "Test Author", 5, 10)
        self.borrowing = Borrowing.objects.create(user=self.user, book=book)

        self.payment = Payment.objects.create(
            borrowing=self.borrowing,
            amount=10.00
        )

    def test_payment_list_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("payments:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_payment_retrieve_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("payments:payment-detail", args=[self.payment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

