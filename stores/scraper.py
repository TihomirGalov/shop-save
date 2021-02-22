import requests
from bs4 import BeautifulSoup
import re

from products.models import Promotion, Product
from .categories import kaufland_cats, billa_cats, lidl_cats

def billa(self):
    response = requests.get(billa_cats[0])
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", 'product')
    promotion, _ = Promotion.objects.get_or_create(store=self)
    for product in products:
        clean = product.get_text().split('\n')
        clean = list(filter(None, clean))
        if len(clean) == 6:
            price = float(clean[-1][:-4])
            pr, _ = Product.objects.get_or_create(name=clean[0], price=price, promotion=promotion)
    return True


def kaufland(self):
    response = requests.get(kaufland_cats[0])
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", 'g-col o-overview-list__list-item')
    promotion, _ = Promotion.objects.get_or_create(store=self)
    for product in products:
        clean = product.get_text().split('\n')
        clean = list(filter(None, clean))
        if len(clean) > 1:
            name = clean[0] + " " + re.sub(r'\t', '', clean[1])
            index = clean.index("Към предложението")
            price = float(re.sub(r'\s', '', clean[index-2]).replace(',', '.'))
            pr, _ = Product.objects.get_or_create(name=name, price=price, promotion=promotion)
    return True


def lidl(self):
    response = requests.get(lidl_cats[0])
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", "product product--tile")
    promotion, _ = Promotion.objects.get_or_create(store=self)
    for product in products:
        clean = product.get_text().split('\n')
        clean = list(filter(None, clean))
        pr, _ = Product.objects.get_or_create(name=clean[0].strip(), price=float(clean[2].strip().replace(',', '.')), promotion=promotion)

