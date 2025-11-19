from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)

from authx.permissions import IsCashier
from .serializers import (
    CreatePurchaseOrderSerializer,
    PurchaseOrderSerializer
)

from .models import PurchaseOrder


class PurchaseViewSet(
        CreateModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        GenericViewSet
    ):
    queryset = PurchaseOrder.objects.all()
    permission_classes = [IsCashier]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "create"]:
            return CreatePurchaseOrderSerializer
        else:
            return PurchaseOrderSerializer