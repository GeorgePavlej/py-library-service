import stripe
from django.conf import settings
from django.core.exceptions import ValidationError

from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(amount):
    if amount <= 0:
        raise ValidationError("Total amount due should be greater than zero")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Library Payment",
                    },
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/api/payments/success",
        cancel_url="http://127.0.0.1:8000/api/payments/cancel",
    )

    return session


def create_stripe_payment(borrowing):
    total_price = borrowing.get_total_borrowing_price()

    try:
        session = create_stripe_session(total_price)
    except ValueError as e:
        raise ValidationError("Invalid total price: {}".format(e))

    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        amount=total_price,
    )

    return payment
