from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    required_role = 1

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role >= self.required_role
        )


class IsCashier(RolePermission):
    required_role = 1


class IsBarista(RolePermission):
    required_role = 2


class IsManager(RolePermission):
    required_role = 3


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == 4 or request.user.is_superuser)
        )


class MenuViewPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if view.action in ["retrieve", "list"]:
            return request.user.role >= 1
            
        elif view.action in ["update", "partial_update", "destroy", "create"]:
            return request.user.role >= 2

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if view.action == "retrieve":
            return request.user.role >= 1

        elif view.action in ["update", "partial_update", "destroy"]:
            return request.user.role >= 2