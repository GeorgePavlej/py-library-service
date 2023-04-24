from typing import Any

from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from borrowings.models import Borrowing
from .models import Payment
from .serializers import PaymentSerializer
from .permissions import IsAdminOrOwner
from .stripe_utils import create_stripe_session


class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing_id = serializer.validated_data["borrowing"].id
        borrowing = Borrowing.objects.get(id=borrowing_id)
        session = create_stripe_session(borrowing)
        amount = serializer.validated_data["amount"]
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


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAdminOrOwner,)


def stripe_success(request):
    return HttpResponse("Payment successful. Thank you for your payment!")


def stripe_cancel(request):
    return HttpResponse("Payment canceled. Please try again later.")
