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
from django.conf.urls import url
from django.utils.html import format_html


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('store', 'expires')


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price', 'product_actions')
    search_fields = ('name',)
    list_filter = ('promotion__store', ExpiredFilter)

    def has_add_permission(self, request):
        return False

    def shop(self, obj):
        return obj.promotion.store

    def add_action(self, request, product_id, *args, **kwargs):
        return self.load_form(
            request=request,
            product_id=product_id,
            action_form=AddToWishlist
        )

    def load_form(self, request, product_id, action_form):
        obj = Product.objects.get(pk=product_id)
        if request.method != "POST":
            form = action_form(obj=obj)
        else:
            form = action_form(request.POST, obj=obj)
        if form.is_valid():
                form.save(obj, request.user)
                url = reverse(
                    "admin:products_product_changelist",
                    current_app="products",
                )
                return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context["opts"] = self.model._meta
        context["form"] = form
        context["title"] = _("Add to Wishlist")
        template = "admin/product/run_action.html"
        return TemplateResponse(
            request,
            template,
            context,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r"^(?P<product_id>.+)/add/$",
                self.admin_site.admin_view(self.add_action),
                name="product-add",
            ),
        ]
        return custom_urls + urls

    def product_actions(self, obj):
        return format_html(f"<a class='button' href=\"{reverse('admin:product-add', args=[obj.pk])}\">{_('Add to Wishlist')}</a>")

    shop.short_description = _("Shop")
    product_actions.short_description = _("Actions")
