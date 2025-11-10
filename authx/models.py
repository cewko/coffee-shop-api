from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

from .common import ROLES
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(max_length=255, unique=True)
    phone = models.PositiveIntegerField(unique=False, null=True, blank=True)

    is_active = models.BooleanField(_("Is active User"), default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    role = models.PositiveIntegerField(
        _("User role"), choices=ROLES, default=1
    )

    join_date = models.DateTimeField(
        _("User Join Date"),
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        _("Last Login Date"),
        null=True, blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return str(self.full_name)


class BlackListToken(models.Model):
    token = models.CharField(
        max_length=500,
        unique=True,
        db_index=True
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="blacklisted_tokens"
    )
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Why was this token blacklisted?"
    )

    class Meta:
        verbose_name = _("Blacklisted Token")
        verbose_name_plural = _("Blacklisted Tokens")
        ordering = ["-blacklisted_at"]

    def __str__(self):
        return f"{self.user.username}'s token"