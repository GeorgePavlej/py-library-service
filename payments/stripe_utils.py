import stripe
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(amount, success_url, cancel_url):
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
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def create_stripe_payment(request, borrowing):
    total_price = borrowing.get_total_borrowing_price()
    success_url = request.build_absolute_uri(reverse("payments:success"))
    cancel_url = request.build_absolute_uri(reverse("payments:cancel"))
    try:
        session = create_stripe_session(total_price, success_url, cancel_url)
    except ValueError as e:
        raise ValidationError("Invalid total price: {}".format(e))

    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        amount=total_price,
    )
    return payment

