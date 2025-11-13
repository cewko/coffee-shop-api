from rest_framework.viewsets import ModelViewSet
from authx.permissions import IsCashier, IsBarista, IsManager
from .serializers import (
    MenuSerializer,
    CashierMenuSerializer,
    MenuItemSerializer,
    CashierMenuItemSerializer,
    ManagerMenuItemSerializer,
    ComponentSerializer,
    ManagerComponentSerializer,
    AdminMenuSerializer
)
from .models import Menu, MenuItem, Component


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    permission_classes = [IsCashier]
    
    def get_serializer_class(self):
        if self.request.user.role == 1:
            return CashierMenuSerializer
        elif self.request.user.role >= 3:
            return AdminMenuSerializer
        else:
            return MenuSerializer


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    permission_classes = [IsCashier]
    
    def get_serializer_class(self):
        if self.request.user.role == 1:
            return CashierMenuItemSerializer
        elif self.request.user.role >= 3:
            return ManagerMenuItemSerializer
        else:
            return MenuItemSerializer


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    permission_classes = [IsBarista]
    
    def get_serializer_class(self):
        if self.request.user.role >= 3:
            return ManagerComponentSerializer
        else:
            return ComponentSerializer