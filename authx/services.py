from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from .jwt import create_jwt
from .models import BlackListToken

User = get_user_model()


class TokenService:
    @staticmethod
    def create_access_token(user: User, expires_in_minutes: int = 60) -> str:
        current_time = now()

        payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": current_time + timedelta(minutes=expires_in_minutes),
            "iat": current_time
        }
        
        return create_jwt(payload)

    @staticmethod
    def blacklist_token(token: str, user: User, reason: str = "") -> BlackListToken:
        return BlackListToken.objects.create(
            token=token,
            user=user,
            reason=reason
        )

    @staticmethod
    def cleanup_expired_tokens():
        pass
    