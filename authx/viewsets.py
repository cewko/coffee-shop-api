from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _

from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import UserSerializer

from utils.mixins import CustomLoggingViewSetMixin

User = get_user_model()


class UserViewSet(CustomLoggingViewSetMixin, ModelViewSet):
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logout(request)
        self.perform_destroy(instance)
        
        return Response(status=HTTP_204_NO_CONTENT)

    def send_auth_email(self, user):
        current_site = get_current_site(self.request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        mail_subject = _("Activate your account")
        protocol = "https" if self.request.is_secure() else "http"

        url = f"{protocol}://{domain}/rest-api/v1/authx/activate/{uid}/{token}"
        message = f"""
        <html>
            <body>
                <h2>Welcome to Coffee Shop!</h2>
                <p>Please click the link below to activate your account:</p>
                <p><a href='{url}'>Activate Account</a></p>
                <p>If the link doesn't work, copy and paste this URL:</p>
                <p>{url}</p>
            </body>
        </html>
        """

        email = EmailMessage(
            subject=mail_subject, 
            body=message, 
            to=[user.email]
        )
        email.send()

    def perform_create(self, serializer):
        super().perform_create(serializer)

        user = serializer.instance
        user.is_active = False
        user.save()

        self.send_auth_email(user)