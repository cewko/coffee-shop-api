from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from datetime import timedelta
from .jwt import create_jwt

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise ValidationError({
                "detail": "Email and password are required"
            })

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("Account is not active.")

        current_time = now()

        payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": current_time + timedelta(minutes=60),
            "iat": current_time     # issued at
        }

        token = create_jwt(payload)

        return Response({
            "jwt": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }, status=HTTP_200_OK)


class ActivationUserEmail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(_(
                "Thank you for your email confirmation. "
                "Now you can login your account."
            ), status=HTTP_200_OK)
        else:
            return Response(_("Activation link is invalid."), status=HTTP_400_BAD_REQUEST)