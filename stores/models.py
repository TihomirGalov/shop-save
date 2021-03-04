from django.db import models
from django.utils.translation import gettext_lazy as _


class Store(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")


