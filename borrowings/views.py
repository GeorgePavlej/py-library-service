from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Borrowing
from .serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingList(generics.ListCreateAPIView):
    serializer_class = BorrowingReadSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)
        queryset = Borrowing.objects.prefetch_related("book")

        if user_id and user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=bool,
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
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BorrowingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReadSerializer
    permission_classes = (IsAuthenticated,)


class BorrowingReturn(views.APIView):
    permission_classes = (IsAuthenticated,)

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
    def post(self, request, *args, **kwargs):
        try:
            borrowing = Borrowing.objects.get(pk=kwargs["pk"])
            borrowing.return_borrowing()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
