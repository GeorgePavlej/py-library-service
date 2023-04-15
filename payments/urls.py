from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path(
        "",
        views.PaymentList.as_view(),
        name="payment-list"
    ),
    path(
        "<int:pk>/",
        views.PaymentDetail.as_view(),
        name="payment-detail"
    ),
]
