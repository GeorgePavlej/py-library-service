import datetime

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from library_service import settings
from payments.models import Payment
from payments.stripe_utils import create_stripe_payment, create_stripe_session


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
    def create_borrowing(cls, request, user, book, borrow_date, expected_return_date):
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
            raise ValidationError(
                "Invalid total price: Total amount due should be greater than zero"
            )

        with transaction.atomic():
            borrowing.save()
            payment = create_stripe_payment(request, borrowing)
        return borrowing

    def return_borrowing(self, is_payment_paid, request=None):
        if self.actual_return_date:
            raise ValueError("Borrowing has already been returned.")
        elif not is_payment_paid:
            raise ValueError("Payment is not completed.")
        else:
            self.actual_return_date = datetime.date.today()
            overdue_days = (self.actual_return_date - self.expected_return_date).days
            if overdue_days > 0:
                fine_amount = overdue_days * self.book.daily_fee * settings.FINE_MULTIPLIER
                fine_payment = Payment.objects.create(
                    borrowing=self,
                    payment_type=Payment.PaymentType.FINE,
                    amount=fine_amount,
                    status=Payment.PaymentStatus.PENDING,
                )
                success_url = (
                    request.build_absolute_uri(reverse("payments:success"))
                    + "?session_id={CHECKOUT_SESSION_ID}"
                )
                cancel_url = request.build_absolute_uri(reverse("payments:cancel"))
                session = create_stripe_session(fine_amount, success_url, cancel_url)
                fine_payment.session_url = session.url
                fine_payment.session_id = session.id
                fine_payment.save()

                return fine_payment
            else:
                self.save()
                return None

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
