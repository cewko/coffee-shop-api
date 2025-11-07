from rest_framework.permissions import BasePermission


class isCashier(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 0)


class IsBarista(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 2)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 3)
    
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 4 or request.user.is_superuser)