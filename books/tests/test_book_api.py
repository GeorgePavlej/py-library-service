import os
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import django


django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
BOOK_URL = reverse("books:book-list")


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_unauthenticated_user_can_read_books(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
