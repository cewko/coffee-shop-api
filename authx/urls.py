from rest_framework.routers import DefaultRouter
from django.urls.conf import include, path
from django.urls import re_path

from .viewsets import UserViewSet
from .views import (
    LoginView, 
    ActivationUserEmail, 
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)

router = DefaultRouter()
router.register(
    r"users",
    UserViewSet,
    basename="users"
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("activate/<str:uidb64>/<str:token>/", ActivationUserEmail.as_view(), name="activate"),
    re_path(r"", include(router.urls))
]