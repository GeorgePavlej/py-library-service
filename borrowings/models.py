import datetime

from django.core.validators import MinValueValidator
from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from payments.stripe_utils import create_stripe_payment


class Borrowing(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    borrow_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today())]
    )
    expected_return_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today())]
    )
    actual_return_date = models.DateField(
        null=True, blank=True, validators=[MinValueValidator(datetime.date.today())]
    )

    def get_total_borrowing_price(self):
        daily_fee = self.book.daily_fee
        borrowing_duration = (self.expected_return_date - self.borrow_date).days
        return daily_fee * borrowing_duration

    @classmethod
    def create_borrowing(cls, user, book, borrow_date, expected_return_date):
        if book.inventory == 0:
            raise ValidationError("This book is out of stock.")

        borrowing = cls(
            user=user,
            book=book,
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
        )

        total_amount_due = borrowing.get_total_borrowing_price()

        if total_amount_due <= 0:
            raise ValidationError("Invalid total price: Total amount due should be greater than zero")

        with transaction.atomic():
            borrowing.save()
            payment = create_stripe_payment(borrowing)
        return borrowing

    def return_borrowing(self):
        if self.actual_return_date:
            raise ValueError("Borrowing has already been returned.")
        else:
            self.actual_return_date = datetime.date.today()
            self.save()

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
