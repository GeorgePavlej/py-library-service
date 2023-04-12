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

    @classmethod
    def create_borrowing(cls, user, book, borrow_date, expected_return_date):
        if book.inventory == 0:
            raise ValueError("This book is out of stock.")
        book.inventory -= 1
        book.save()
        borrowing = cls(user=user, book=book, borrow_date=borrow_date, expected_return_date=expected_return_date)
        borrowing.save()
        return borrowing

    def return_borrowing(self):
        if self.actual_return_date:
            raise ValueError("Borrowing has already been returned.")
        else:
            self.actual_return_date = datetime.date.today()
            self.book.inventory += 1
            self.book.save()
            self.save()

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
