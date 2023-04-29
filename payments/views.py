from typing import Any

from django.http import HttpResponse
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
    permission_classes = (permissions.IsAuthenticated, IsAdminOrOwner,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]

        if amount <= 0:
            return Response(
                {"detail": "The total amount due cannot be zero or negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = create_stripe_session(amount)
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


def stripe_success(request):
    return HttpResponse("Payment successful. Thank you for your payment!")


def stripe_cancel(request):
    return HttpResponse("Payment canceled. Please try again later.")
