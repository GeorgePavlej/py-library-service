from django.urls import path

from borrowings.views import (
    BorrowingList,
    BorrowingDetail,
    BorrowingReturn
)

app_name = "borrowings"

urlpatterns = [
    path("", BorrowingList.as_view(), name="borrowing-list"),
    path(
        "<int:pk>/",
        BorrowingDetail.as_view(),
        name="borrowing-detail"),
    path(
        "<int:pk>/return/",
        BorrowingReturn.as_view(),
        name="borrowing-return",
    ),
]
