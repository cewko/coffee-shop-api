from django.db import models


class Component(models.Model):
    ingredient = models.ForeignKey(
        "storage.Ingredient",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

    @property
    def name(self):
        return "{} - {} - {}".format(
            self.ingredient.name,
            self.quantity,
            self.ingredient.get_unit_display()
        )

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    price_net = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField(
        Component,
        blank=True
    )
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=23)

    @property
    def price_gross(self):
        return round(self.price_net * (1 + self.tax / 100), 2)

    def __str__(self):
        return f"{self.name} {self.price_gross} PLN"


class Menu(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    items = models.ManyToManyField(MenuItem)

