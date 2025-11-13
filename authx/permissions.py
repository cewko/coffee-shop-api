from rest_framework.permissions import BasePermission


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 1)


class IsBarista(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 2)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 3)
    

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 4 or request.user.is_superuser)


class MenuViewPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["retrieve", "list"]:
            return bool(request.user.is_authenticated and request.user.role >= 1)
        elif view.action in ["update", "partial_update", "destroy", "create"]:
            return bool(request.user.is_authenticated and request.user.role >= 2)

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return bool(request.user.is_authenticated and request.user.role >= 1)
        elif view.action in ["update", "partial_update", "destroy", "create"]:
            return bool(request.user.is_authenticated and request.user.role >= 2)