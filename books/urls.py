from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "books"

router = DefaultRouter()
router.register("", views.BookViewSet)

urlpatterns = [path("", include(router.urls))]
