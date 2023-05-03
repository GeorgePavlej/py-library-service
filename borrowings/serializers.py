from rest_framework import serializers

from payments.serializers import PaymentSerializer
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

    def validate(self, data):
        if data["expected_return_date"] <= data["borrow_date"]:
            raise serializers.ValidationError(
                "Expected return date must be greater than the borrow date."
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        request = self.context["request"]
        return Borrowing.create_borrowing(user=user, request=request, **validated_data)
