from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from payments.serializers import PaymentSerializer
from payments.stripe_utils import create_stripe_payment
from .models import Borrowing
from books.models import Book


class BorrowingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BorrowingBookSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "payments",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "book",
            "borrow_date",
            "expected_return_date",
        )

    def validate(self, data: dict) -> dict:
        if data["expected_return_date"] <= data["borrow_date"]:
            raise serializers.ValidationError(
                "Expected return date must be greater than the borrow date."
            )
        return data

    def create(self, validated_data: dict) -> Borrowing:
        user = self.context["request"].user
        book = validated_data["book"]
        borrow_date = validated_data["borrow_date"]
        expected_return_date = validated_data["expected_return_date"]

        if book.inventory == 0:
            raise ValidationError("This book is out of stock.")

        borrowing = Borrowing(
            user=user,
            book=book,
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
        )

        total_amount_due = borrowing.get_total_borrowing_price()

        if total_amount_due <= 0:
            raise ValidationError(
                "Invalid total price: "
                "Total amount due should be greater than zero"
            )

        with transaction.atomic():
            borrowing.save()
            payment = create_stripe_payment(self.context["request"], borrowing)
        return borrowing
