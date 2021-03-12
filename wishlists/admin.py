from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Wishlist, WishlistItem


class WishlistItemAdmin(admin.TabularInline):
    model = WishlistItem
    extra = 1


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishlistItemAdmin,)
    list_display = ("name", "pr_num", "total_price", "wishlist_actions")
    fields = ("name",)

    def pr_num(self, obj):
        return obj.items.all().count()

    def buy_wishlist(self, request, wishlist_id, *args, **kwargs):
        obj = Wishlist.objects.get(pk=wishlist_id)
        obj.bought = True
        obj.save()
        url = reverse(
            "admin:wishlists_wishlist_changelist",
            current_app="wishlists",
        )
        return HttpResponseRedirect(url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r"^(?P<wishlist_id>.+)/buy/$",
                self.admin_site.admin_view(self.buy_wishlist),
                name="wishlist-buy",
            ),
        ]
        return custom_urls + urls

    def wishlist_actions(self, obj):
        if not obj.bought:
            return format_html(f"<a class='button' href=\"{reverse('admin:wishlist-buy', args=[obj.pk])}\">{_('Buy')}</a>")

    pr_num.short_description = _("Number of Items")
    wishlist_actions.short_description = _("Actions")