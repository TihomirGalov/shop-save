from jet.dashboard.dashboard import Dashboard
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from wishlists.dashboard_modules import WishlistChart


class ShopAndSaveDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(WishlistChart)

        self.children.append(WishlistChart())
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=0,
            order=0
        ))
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=0,
            order=0
        ))
