from django import forms
from django.utils.translation import gettext_lazy as _

from wishlists.models import Wishlist, WishlistItem


class ActionForm(forms.Form):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj

    def form_action(self, obj, user):
        raise NotImplementedError()

    def save(self, obj=None, user=None):
        try:
            self.form_action(obj, user)
        except Exception as e:
            print(e)
            error_message = str(e)
            self.add_error(None, error_message)
            raise


class AddToWishlist(ActionForm):
    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.fields["wishlist"] = forms.ModelChoiceField(
            queryset=Wishlist.objects.all()
        )
        self.fields[obj.name] = forms.DecimalField(label_suffix=f"({_('Quantity')})")

    def form_action(self, obj, user):
        wishlist = self.cleaned_data.get("wishlist")
        wi = WishlistItem(wishlist=wishlist, product=obj, amount=self.cleaned_data.get(obj.name))
        wi.save()
