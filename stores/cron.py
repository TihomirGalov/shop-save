import datetime
from .models import Store
from .scraper import kaufland, billa, lidl


def get_data():
    for store in Store.objects.all():
        if store.promotions.last().expires <= datetime.datetime.now():
            if store.name == "Billa":
                billa(store)
            if store.name == "Kaufland":
                kaufland(store)
            if store.name == "Lidl":
                lidl(store)