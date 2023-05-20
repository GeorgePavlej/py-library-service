from typing import Any

import stripe
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import (
    permissions,
    status,
    viewsets
)
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from .permissions import IsAdminOrOwner
from .stripe_utils import create_stripe_session


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrOwner,
    )

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]

        success_url = request.build_absolute_uri(reverse("payments:success"))
        cancel_url = request.build_absolute_uri(reverse("payments:cancel"))

        session = create_stripe_session(amount, success_url, cancel_url)
        serializer.validated_data["session_url"] = session.url
        serializer.validated_data["session_id"] = session.id

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self) -> Any:
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing__user=user)


def stripe_success(request: HttpRequest) -> HttpResponse:
    session_id = request.GET.get("session_id")
    payment = get_object_or_404(Payment, session_id=session_id)

    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        payment.status = Payment.PaymentStatus.PAID
        payment.save()
        return HttpResponse("Payment successful. Thank you for your payment!")
    else:
        return HttpResponse("Payment not successful. Please try again.")


def stripe_cancel(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Payment canceled. Please try again later. "
        "Note that the payment session is only available for 24 hours."
    )
