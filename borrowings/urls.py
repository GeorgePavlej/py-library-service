from django.urls import path, include
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingViewSet

app_name = "borrowings"

router = DefaultRouter()
router.register("", BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:pk>/return-borrowing/",
        BorrowingViewSet.as_view({"post": "return_borrowing"}),
        name="return-borrowing",
    ),
]
