from django.contrib import admin
from .models import Store
from django.utils.html import format_html


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)
