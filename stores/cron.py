import datetime
from .models import Store
from .scraper import kaufland, billa, lidl


def get_data():
    for store in Store.objects.all():
        if store.promotions.filter(expires__lte=datetime.datetime.now()).count() == store.promotions.all().count():
            if store.name == "Billa":
                billa(store)
            if store.name == "Kaufland":
                kaufland(store)
            if store.name == "Lidl":
                lidl(store)