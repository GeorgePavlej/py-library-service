from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "borrowing",
            "amount",
            "session_url",
        )

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError(
                "The total amount due cannot be zero or negative."
            )
        return value
