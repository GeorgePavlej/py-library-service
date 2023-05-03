from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    stripe_success,
    stripe_cancel,
    PaymentViewSet
)

app_name = "payments"

router = DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("success/", stripe_success, name="success"),
    path("cancel/", stripe_cancel, name="cancel"),
] + router.urls
