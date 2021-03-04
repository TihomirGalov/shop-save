import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, related_name='promotions', verbose_name=_("Store"))
    expires = models.DateTimeField(default=datetime.datetime.today(), verbose_name=_("Expires"))

    def __str__(self):
        return f"{self.store} {self.expires}"

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")


class Product(models.Model):
    promotion = models.ForeignKey(Promotion, related_name='products', on_delete=models.CASCADE, verbose_name=_("Promotion"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Porduct")
        verbose_name_plural = _("Products")