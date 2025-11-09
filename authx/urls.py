from rest_framework.routers import DefaultRouter
from django.urls.conf import include, path
from django.urls import re_path

from .viewsets import UserViewSet
from .views import LoginView, ActivationUserEmail


router = DefaultRouter()
router.register(
    r"users",
    UserViewSet,
    basename="users"
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("activate/<slug:uidb64>/<slug:token>/", ActivationUserEmail.as_view(), name="activate"),
    re_path(r"", include(router.urls))
]