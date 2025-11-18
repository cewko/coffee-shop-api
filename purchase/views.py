from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .serializers import ListPurchaseOrderSerializer
from .models import PurchaseOrder


class PurchaseListView(ListAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = ListPurchaseOrderSerializer
    permission_classes = [AllowAny]