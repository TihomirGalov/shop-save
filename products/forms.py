from django import forms
from wishlists.models import Wishlist, WishlistItem
from django.utils.translation import gettext_lazy as _


class ActionForm(forms.Form):
    def __init__(self, *args, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = queryset

    def form_action(self, queryset, user):
        raise NotImplementedError()

    def save(self, queryset=None, user=None):
        try:
            self.form_action(queryset, user)
        except Exception as e:
            print(e)
            error_message = str(e)
            self.add_error(None, error_message)
            raise


class AddToWishlist(ActionForm):
    def __init__(self, queryset, *args, **kwargs):
        super().__init__(queryset=queryset, *args, **kwargs)
        self.fields["wishlist"] = forms.ModelChoiceField(
            queryset=Wishlist.objects.all(), required=False
        )
        for pr in queryset:
            self.fields[pr.name] = forms.DecimalField(label_suffix=f" {_('quantity')}")

    def form_action(self, queryset, user):
        wishlist = self.cleaned_data.get("wishlist")
        for pr in queryset:
            wi = WishlistItem(wishlist=wishlist, product=pr, amount=self.cleaned_data.get(pr.name))
            wi.save()
