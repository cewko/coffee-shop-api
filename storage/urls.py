from django.urls.conf import include
from django.urls import re_path

from rest_framework.routers import DefaultRouter
from .viewsets import IngredientViewSet


router = DefaultRouter()
router.register(
    r"",
    IngredientViewSet,
    basename="ingredients"
)

urlpatterns = [
    re_path(r"", include(router.urls))
]