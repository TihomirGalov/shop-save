from django.db import models
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField

from products.models import Product


class Wishlist(models.Model):
    user = CurrentUserField(verbose_name=_("User"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    bought = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        total_sum = 0
        for item in self.items.all():
            total_sum += item.price
        return total_sum

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items", verbose_name=_("Wishlist"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items",
                                verbose_name=_("Product"))
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=1, verbose_name=_("Quantity"))

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        return round(self.product.price * self.amount, 2)

    class Meta:
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlists Items")
