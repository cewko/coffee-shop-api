from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.status import HTTP_200_OK
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
