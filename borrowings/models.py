import datetime

from django.core.validators import MinValueValidator
from django.db import models


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
        null=True, blank=True, validators=[
            MinValueValidator(datetime.date.today())
        ]
    )

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
