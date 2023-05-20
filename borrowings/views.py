from datetime import date
from typing import Type

from django.db.models import QuerySet
from django.urls import reverse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from library_service import settings
from payments.models import Payment
from payments.stripe_utils import create_stripe_session
from .models import Borrowing
from .serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.request.method == "POST":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=str,
                enum=["true", "false"],
                description="Filter by active borrowings (ex. ?is_active=true)",
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="user_id",
                type=int,
                description=(
                    "Filter by user id (for admin users only, ex. ?user_id=2)"
                ),
                location=OpenApiParameter.QUERY,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Borrowing]:
        user = self.request.user
        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)
        queryset = Borrowing.objects.prefetch_related("book")

        if user_id and user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        return queryset

    @action(detail=True, methods=["post"])
    def return_borrowing(self, request: Request, *args, **kwargs) -> Response:
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"detail": "Borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        payment_status = borrowing.payments.first().status
        is_payment_paid = payment_status == Payment.PaymentStatus.PAID
        if not is_payment_paid:
            return Response(
                {"detail": "Payment is not completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.actual_return_date = date.today()
        overdue_days = (
                borrowing.actual_return_date - borrowing.expected_return_date
        ).days
        if overdue_days > 0:
            fine_amount = overdue_days * borrowing.book.daily_fee \
                          * settings.FINE_MULTIPLIER
            fine_payment = Payment.objects.create(
                borrowing=borrowing,
                payment_type=Payment.PaymentType.FINE,
                amount=fine_amount,
                status=Payment.PaymentStatus.PENDING,
            )
            success_url = (
                    request.build_absolute_uri(reverse("payments:success"))
                    + "?session_id={CHECKOUT_SESSION_ID}"
            )
            cancel_url = request.build_absolute_uri(
                reverse("payments:cancel")
            )
            session = create_stripe_session(
                fine_amount, success_url, cancel_url
            )
            fine_payment.session_url = session.url
            fine_payment.session_id = session.id
            fine_payment.save()

            return Response(
                {
                    "detail": "Fine payment created.",
                    "payment_id": fine_payment.id,
                    "payment_url": fine_payment.session_url,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            borrowing.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
