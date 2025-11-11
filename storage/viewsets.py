from rest_framework.viewsets import ModelViewSet
from authx.permissions import IsBarista, IsManager

from .serializers import (
    BaristaIngredientSerializer,
    ManagerIngredientSerializer
)
from .models import Ingredient


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsBarista]

    def get_serializer_class(self):
        permission = IsManager()
        if permission.has_permission(self.request, self):
            return ManagerIngredientSerializer
            
        return BaristaIngredientSerializer