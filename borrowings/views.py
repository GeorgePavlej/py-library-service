from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from payments.models import Payment
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
    @extend_schema(
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "description": "Not Found",
                    },
                },
            },
            status.HTTP_400_BAD_REQUEST: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "description": "Borrowing has already been returned.",
                    },
                },
            },
        },
    )
    def return_borrowing(self, request: Request, *args, **kwargs) -> Response:
        try:
            borrowing = Borrowing.objects.get(pk=kwargs["pk"])
            payment_status = borrowing.payments.first().status
            is_payment_paid = payment_status == Payment.PaymentStatus.PAID
            fine_payment = borrowing.return_borrowing(
                is_payment_paid, request=request
            )
            if fine_payment:
                return Response(
                    {
                        "detail": "Fine payment created.",
                        "payment_id": fine_payment.id,
                        "payment_url": fine_payment.session_url,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {
                    "detail": "Borrowing not found."
                }, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as error:
            return Response({
                "detail": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
