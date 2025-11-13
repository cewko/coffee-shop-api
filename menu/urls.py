from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    MenuViewSet,
    MenuItemViewSet,
    ComponentViewSet
)

router = DefaultRouter()

router.register(
    r"menus",
    MenuViewSet,
    basename="menu"
)

router.register(
    r"items",
    MenuItemViewSet,
    basename="menuitem"
)

router.register(
    r"components",
    ComponentViewSet,
    basename="component"
)

urlpatterns = [
    path("", include(router.urls))
]