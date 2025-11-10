from datetime import timedelta

from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.timezone import now
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from .jwt import create_jwt
from .models import BlackListToken

User = get_user_model()


class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]
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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token.startswith("Bearer "):
            token = token[7:]

        BlackListToken.objects.create(
            token=token,
            user=request.user,
            reason="user logout"
        )

        return Response(
            {"detail": _("Successfully logged out")},
            status=HTTP_200_OK
        )


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")

        if not email:
            raise ValidationError({"detail": "Email is required"})

        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            try:
                current_site = get_current_site(request)
                domain = current_site.domain
            except:
                domain = request.get_host()

            protocol = "https" if request.is_secure() else "http"
            reset_url = f"{protocol}://{domain}/rest-api/v1/authx/password-reset-confirm/{uid}/{token}"

            mail_subject = _("Reset Your Password")
            message = f"""
            <html>
                <body>
                    <h2>Password Reset Request</h2>
                    <p>Hello {user.username},</p>
                    <p>You requested to reset your password. Click the link below to reset it:</p>
                    <p><a href='{reset_url}'>Reset Password</a></p>
                    <p>If you didn't request this, please ignore this email.</p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If the link doesn't work, copy and paste this URL:</p>
                    <p>{reset_url}</p>
                </body>
            </html>
            """

            try:
                email_message = EmailMessage(
                    subject=mail_subject,
                    body=message,
                    to=[user.email]
                )
                email_message.content_subtype = "html"
                email_message.send()
            except Exception as error:
                print(f"Failed to send password reset link: {error}")

        return Response(
            {"detail": _("If that email exists, a password reset link has been sent.")},
            status=HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, uidb64, token):
        new_password = request.data.get("new_password")
        
        if not new_password:
            raise ValidationError({"detail": "New password is required"})

        if len(new_password) < 8:
            raise ValidationError({"detail": "Password must be at least 8 characters"})
 
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            raise ValidationError({"detail": _("Invalid reset link")})

        is_valid = default_token_generator.check_token(user, token)
        
        if not is_valid:
            raise ValidationError({"detail": _("Invalid or expired reset link")})

        user.set_password(new_password)
        user.save()
        
        return Response(
            {"detail": _("Password has been reset successfully. You can now login with your new password.")},
            status=HTTP_200_OK
        )

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