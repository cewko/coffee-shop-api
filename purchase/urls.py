from django.urls.conf import include
from django.urls import re_path, path

from rest_framework.routers import DefaultRouter
from .views import PurchaseListView, CancellingPurchase
from .viewsets import PurchaseViewSet

router = DefaultRouter()
router.register(
    r"purchase",
    PurchaseViewSet,
    basename="purchase"
)

urlpatterns = [
    path("list/", PurchaseListView.as_view(), name="purchase-list"),
    path("cancel/<int:pk>/", CancellingPurchase.as_view(), name="purchase-cancel"),
    re_path(r"", include(router.urls))
]