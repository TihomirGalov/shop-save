from django.contrib import admin
from .models import Wishlist, WishlistItem
from django.utils.translation import gettext_lazy as _


class WishlistItemAdmin(admin.TabularInline):
    model = WishlistItem
    extra = 1


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishlistItemAdmin,)
    list_display = ("name", "pr_num", "total_price")
    fields = ("name",)

    def pr_num(self, obj):
        return obj.items.all().count()

    pr_num.short_description = _("Number of Items")


