from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .jwt import decode_jwt
from .models import BlackListToken

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"
    
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        
        if not auth_header:
            return None
        
        token = self.get_token_from_header(auth_header)
        
        if not token:
            return None
        
        if self.is_token_blacklisted(token):
            raise AuthenticationFailed(
                _("Token has been revoked"),
                code="token_revoked"
            )
        
        try:
            payload = decode_jwt(token)
        except ValueError as error:
            raise AuthenticationFailed(
                str(error),
                code="invalid_token"
            )
        
        user = self.get_user_from_payload(payload)
        
        return user, token
    
    def get_token_from_header(self, auth_header: str) -> str:
        parts = auth_header.split()
        
        if len(parts) == 0:
            return None
        
        if parts[0] != self.keyword:
            return None
        
        if len(parts) == 1:
            raise AuthenticationFailed(
                _("Invalid authorization header. No credentials provided.")
            )
        elif len(parts) > 2:
            raise AuthenticationFailed(
                _("Invalid authorization header. Token should not contain spaces.")
            )
        
        return parts[1]
    
    def is_token_blacklisted(self, token: str) -> bool:
        return BlackListToken.objects.filter(token=token).exists()
    
    def get_user_from_payload(self, payload: dict) -> User:
        user_id = payload.get("id")
        
        if not user_id:
            raise AuthenticationFailed(
                _("Token payload invalid"),
                code="invalid_payload"
            )
        
        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                _("User not found or inactive"),
                code="user_not_found"
            )
        
        return user