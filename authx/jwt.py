import base64
import json
import hmac
import hashlib

from datetime import datetime, timezone
from django.conf import settings


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def base64url_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    
    if padding != 4:
        data += "=" * padding

    return base64.urlsafe_b64decode(data)


def create_jwt(payload: dict) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    if "exp" in payload and isinstance(payload["exp"], datetime):
        payload["exp"] = int(payload["exp"].timestamp())

    if "iat" in payload and isinstance(payload["iat"], datetime):
        payload["iat"] = int(payload["iat"].timestamp())

    header_encoded = base64url_encode(json.dumps(
        header, separators=(",", ":")
    ).encode())

    payload_encoded = base64url_encode(json.dumps(
        payload, separators=(",", ":")
    ).encode())

    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()

    signature_encoded = base64url_encode(signature)

    return f"{message}.{signature_encoded}"


def decode_jwt(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        header_encoded, payload_encoded, signature_encoded = parts

        message = f"{header_encoded}.{payload_encoded}"
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()

        provided_signature = base64url_decode(signature_encoded)

        if not hmac.compare_digest(expected_signature, provided_signature):
            raise ValueError("Invalid signature")

        payload_json = base64url_decode(payload_encoded)
        payload = json.loads(payload_json)

        if "exp" in payload:
            exp_timestamp = payload["exp"]
            if datetime.now(timezone.utc).timestamp() > exp_timestamp:
                raise ValueError("Token has expired")

        return payload

    except Exception as error:
        raise ValueError(f"Token validation failed {error}")