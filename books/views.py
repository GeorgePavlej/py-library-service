from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Book.objects.all()
        title = self.request.query_params.get("title")
        if title is not None:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by books title",
                required=False,
                type=str,
            ),
        ],
    )
    def list(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Filter books by title"""
        return super().list(request, *args, **kwargs)
