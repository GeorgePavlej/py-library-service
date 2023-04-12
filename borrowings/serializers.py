from rest_framework import serializers
from .models import Borrowing
from books.models import Book


class BorrowingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BorrowingBookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book", "borrow_date", "expected_return_date")

    def create(self, validated_data):
        user = self.context["request"].user
        return Borrowing.create_borrowing(user=user, **validated_data)
