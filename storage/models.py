from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    UNIT_CHOICES = (
        (1, _("ml")),
        (2, _("g"))
    )

    name = models.CharField(
        _("Ingredient Name"),
        max_length=50, 
        null=False, 
        blank=False
    )
    sku_number = models.CharField(
        _("SKU Number"),
        max_length=50, 
        unique=True,
    )
    quantity = models.IntegerField(_("Quantity"), default=0)
    supplier = models.ForeignKey(
        "supplier.Supplier",
        on_delete=models.SET_NULL,
        null=True
    )
    unit = models.PositiveSmallIntegerField(
        choices=UNIT_CHOICES,
        default=1
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} - {self.quantity}{self.get_unit_display()}"
