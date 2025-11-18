from django.urls.conf import include
from django.urls import re_path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    re_path(r"", include(router.urls))
]