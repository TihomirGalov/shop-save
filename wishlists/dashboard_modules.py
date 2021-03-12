import plotly.graph_objs as go
from django.db.models import F
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django_currentuser.middleware import get_current_user
from jet.dashboard.modules import DashboardModule
from plotly.offline import plot

from .models import Wishlist


class WishlistChart(DashboardModule):
    title = _("Bought Wishlists")
    template = "admin/graph.html"

    def init_with_context(self, context):
        fig = go.Figure()
        updatemenus = [{"buttons": []}]

        wishlists = Wishlist.objects.filter(user=get_current_user()).filter(bought=True)
        count = wishlists.count()

        index = 0
        for wishlist in wishlists:
            fig.add_trace(
                go.Pie(
                    name=wishlist.name,
                    labels= list(wishlist.items.all().values_list("product__name", flat=True)),
                    values=[wi.price for wi in wishlist.items.all()],
                    visible=(index == 0),
                )
            )
            updatemenus[0]["buttons"].append(
                dict(
                    label=f"{wishlist.name}",
                    method="update",
                    args=[
                        {"visible": [index == i for i in range(count)]},
                        {
                            "title": gettext("Show for ")
                                     + f"{wishlist.name}"
                        },
                    ],
                )
            )
            index = index + 1

        fig.update_layout(
            title=gettext("Wishlists"),
            showlegend=False,
            updatemenus=updatemenus,
        )
        div = plot(fig, auto_open=False, output_type="div")

        self.graph = div
