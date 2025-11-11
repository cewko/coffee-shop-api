from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator


class Supplier(models.Model):
    name = models.CharField(
        _("Supplier Name"),
        max_length=50,
        validators=[MinLengthValidator(4)],
        null=False,
        blank=False
    )
    phone_regex = RegexValidator(
        regex=r"^\+?[\d]{4,15}$",
        message="Phone number must be entered in the format: '+49301234567', \
            Up to 15 digits is allowed."
    )
    phone_number = models.CharField(
        _("Phone number"),
        validators=[phone_regex],
        max_length=17,
        blank=False,
        null=False
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-name",)
    
    @property
    def custom_id(self):
        phone_part = self.phone_number.replace("+", "")[-2:]
        name_part = self.name[:2].upper()
        year = self.created_date.year

        return f"{phone_part}-{name_part}-{year}"

    def __str__(self):
        return self.custom_id
