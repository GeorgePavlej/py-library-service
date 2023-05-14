from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from books.models import Book
from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = Book.objects.all()
        title = self.request.query_params.get("title")
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                description="Filter by books title",
                required=False,
                type=str,
            ),
        ],
    )
    def list(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Filter books by title"""
        return super().list(request, *args, **kwargs)
