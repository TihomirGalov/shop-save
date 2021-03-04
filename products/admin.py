from django.contrib import admin
from .models import Promotion, Product
from django.utils.translation import gettext_lazy as _


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price')
    search_fields = ('name',)
    list_filter = ('promotion__store',)

    def has_add_permission(self, request):
        return False

    def shop(self, obj):
        return obj.promotion.store

    shop.short_description = _("Shop")
