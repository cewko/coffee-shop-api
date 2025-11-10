import json
import hmac
import hashlib

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from datetime import datetime
from .jwt import decode_jwt


User = get_user_model()


class TokenAuthentication(BaseAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")

        if token is None:
            return None

        if token.startswith("Bearer "):
            token = token[7:]

        segments = token.split(".")

        if len(segments) != 3:
            raise AuthenticationFailed(
                _("Authorization header must contain three space-delimited values"),
                code="bad_authorization_header"
            )

        if not segments[1]:
            raise AuthenticationFailed(
                _("Token payload is empty"),
                code="invalid_token"
            )

        if not self.verify_signature(segments[0], segments[1], segments[2]):
            raise AuthenticationFailed(
                _("Invalid token signature"),
                code="invalid_signature"
            )

        try:
            validated_token = decode_jwt(segments[1])
        except Exception as error:
            raise AuthenticationFailed(
                _("Token could not be decoded"),
                code="invalid_token"
            )

        return self.get_user(validated_token), validated_token

    def verify_signature(self, header, payload, signature):
        message = f"{header}.{payload}"
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        try:
            decoded_signature = decode_jwt(signature).decode("utf-8")
        except Exception:
            return False

        return hmac.compare_digest(expected_signature, decoded_signature)

    def get_user(self, validated_token):
        res = json.loads(validated_token)
        exp = res.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.now():
            raise AuthenticationFailed("Token has expired")
        
        try:
            user_id = res.get("id")
        except KeyError:
            raise ValidationError(_("No user id"))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                _("User not found"),
                code="user_not_found"
            )

        if not user.is_active:
            raise AuthenticationFailed(
                _("User account is disabled"),
                code="user_inactive"
            )

        return user