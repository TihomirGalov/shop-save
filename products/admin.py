from django.contrib import admin
from .models import Promotion, Product


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price')

    def shop(self, obj):
        return obj.promotion.store