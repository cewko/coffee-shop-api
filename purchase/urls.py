from django.urls.conf import include
from django.urls import re_path, path

from rest_framework.routers import DefaultRouter
from .views import PurchaseListView
from .viewsets import PurchaseViewSet

router = DefaultRouter()
router.register(
    r"purchase",
    PurchaseViewSet,
    basename="purchase"
)

urlpatterns = [
    re_path(r"", include(router.urls)),
    path("purchase-list", PurchaseListView.as_view(), name="purchase-list")
]