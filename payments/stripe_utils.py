import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(borrowing):
    total_price = borrowing.get_total_borrowing_price()
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Library Payment",
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/api/payments/success",
        cancel_url="http://127.0.0.1:8000/api/payments/cancel",
    )

    return session
