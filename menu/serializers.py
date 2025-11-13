from rest_framework.serializers import ModelSerializer, SlugRelatedField
from storage.serializers import BaristaIngredientSerializer, ManagerIngredientSerializer

from .models import Menu, MenuItem, Component


class BaseComponentSerializer(ModelSerializer):
    class Meta:
        model = Component
        fields = "__all__"


class BaseItemSerializer(ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

    
class BaseMenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class ManagerComponentSerializer(BaseComponentSerializer):
    ingredient = ManagerIngredientSerializer(read_only=True)


class ComponentSerializer(BaseComponentSerializer):
    ingredient = BaristaIngredientSerializer(read_only=True)


class MenuItemSerializer(BaseItemSerializer):
    ingredients = ComponentSerializer(read_only=True, many=True)


class ManagerMenuItemSerializer(BaseItemSerializer):
    ingredients = ManagerComponentSerializer(read_only=True, many=True)


class CashierMenuItemSerializer(BaseItemSerializer):
    ingredients = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class MenuSerializer(BaseMenuSerializer):
    items = MenuItemSerializer(read_only=True, many=True)


class AdminMenuSerializer(BaseMenuSerializer):
    items = ManagerManuItemSerializer(read_only=True, many=True)


class CashierMenuSerializer(BaseMenuSerializer):
    items = CashierMenuItemSerializer(read_only=True, many=True)