from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from authx.permissions import IsCashier
from .serializers import ListPurchaseOrderSerializer, PurchaseOrderSerializerCancelling
from .models import PurchaseOrder


class PurchaseListView(ListAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = ListPurchaseOrderSerializer
    permission_classes = [AllowAny]


class CancellingPurchase(APIView):
    permission_classes = [IsCashier]

    def _get_purchase_id(self):
        return self.kwargs.get("pk", None)

    def _get_purchase(self):
        obj = get_object_or_404(PurchaseOrder, id=self._get_purchase_id())
        return obj

    def patch(self, request, *args, **kwargs):
        purchase = self._get_purchase()
        self.check_object_permissions(request, purchase)
        purchase.created_by = request.user
        purchase.items.set([])
        purchase.status = 5
        purchase.save()

        response = PurchaseOrderSerializerCancelling(purchase, many=False)
        return Response(response.data, status=HTTP_200_OK)