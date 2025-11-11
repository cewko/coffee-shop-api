from rest_framework.viewsets import ModelViewSet
from authx.permissions import IsManager, IsCashier
from .serializers import AdminSupplierSerializer, SupplierSerializer
from .models import Supplier


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    
    def get_serializer_class(self):
        permission = IsManager()
        if permission.has_permission(self.request, self):
            return AdminSupplierSerializer
        return SupplierSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsManager()]
        return [IsCashier()]