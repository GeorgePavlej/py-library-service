import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Borrowing(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    borrow_date = models.DateField(
        default=timezone.now,
        validators=[MinValueValidator(datetime.date.today())]
    )
    expected_return_date = models.DateField(
        default=timezone.now,
        validators=[MinValueValidator(datetime.date.today())]
    )
    actual_return_date = models.DateField(
        null=True,
        blank=True,
        validators=[MinValueValidator(datetime.date.today())]
    )

    def get_total_borrowing_price(self) -> float:
        daily_fee = self.book.daily_fee
        borrowing_duration = (
                self.expected_return_date - self.borrow_date
        ).days
        return daily_fee * borrowing_duration

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
