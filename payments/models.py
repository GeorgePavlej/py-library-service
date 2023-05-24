from django.db import models


class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class PaymentType(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_type = models.CharField(
        max_length=10,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT
    )
    borrowing = models.ForeignKey(
        "borrowings.Borrowing",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    updated_at = models.DateTimeField(auto_now=True)
    session_url = models.URLField(max_length=360, blank=True, null=True)
    session_id = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.borrowing.user.email} - {self.payment_type}"
