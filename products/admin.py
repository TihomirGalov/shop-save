import datetime
from django.contrib import admin
from .models import Promotion, Product
from django.utils.translation import gettext_lazy as _
from .forms import AddToWishlist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse
from django.conf import settings
import os


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


class ExpiredFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Expired')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (True, _('Expired')),
            (False, _('Active')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(promotion__expires__lte=datetime.datetime.now())
        else:
            return queryset.filter(promotion__expires__gte=datetime.datetime.now())


def add_to_wishlist(modeladmin, request, queryset):
    if request.method != "POST":
        form = AddToWishlist(queryset=queryset)
    else:
        form = AddToWishlist(queryset=queryset)
        if form.is_valid():
            form.save(queryset, request.user)
            url = reverse(
                "admin:products_product_changelist",
                current_app="products",
            )
            return HttpResponseRedirect(url)
    context = modeladmin.admin_site.each_context(request)
    context["opts"] = modeladmin.model._meta
    context["form"] = form
    context["title"] = "Add to Wishlist"
    template = os.path.join(settings.BASE_DIR, "products/templates/admin/product/run_action.html")

    return TemplateResponse(
        request,
        template,
        context,
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price')
    search_fields = ('name',)
    list_filter = ('promotion__store', ExpiredFilter)
    actions = [add_to_wishlist]

    def has_add_permission(self, request):
        return False

    def shop(self, obj):
        return obj.promotion.store

    shop.short_description = _("Shop")
