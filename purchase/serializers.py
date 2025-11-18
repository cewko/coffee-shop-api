from datetime import datetime
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CharField
)

from .models import PurchaseOrder
from menu.models import MenuItem
from menu.serializers import CashierMenuItemSerializer

class ListPurchaseOrderSerializer(ModelSerializer):
    status = CharField(source="get_status_display")
    
    class Meta:
        model = PurchaseOrder
        fields = ["status", "order_number"]


class PurchaseOrderSerializer(ModelSerializer):
    items = CashierMenuItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class CreatePurchaseOrderSerializer(PurchaseOrderSerializer):
    items = PrimaryKeyRelatedField(
        many=True,
        queryset=MenuItem.objects.all()
    )

    def to_internal_value(self, data):
        today = datetime.now()
        count_today = PurchaseOrder.objects.filter(
            created_date__date=today.date()
        ).count() + 1
        data["order_number"] = f"{today.strftime('%d%m%y')}_{count_today}"

        return super().to_internal_value(data)