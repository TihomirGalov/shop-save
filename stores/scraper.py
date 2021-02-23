import datetime
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
    expires = soup.find("div", 'date').get_text().split(" ")[-2]
    promotion, _ = Promotion.objects.get_or_create(store=self, expires=datetime.datetime.strptime(expires, '%d.%m.%Y'))
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
    expires = soup.find("div", 'a-icon-tile-headline__subheadline').get_text().split(" ")[-1]
    promotion, _ = Promotion.objects.get_or_create(store=self, expires=datetime.datetime.strptime(expires[:-2], '%d.%m.%Y'))

    for category in kaufland_cats[1:]:
        response = requests.get(category)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", 'g-col o-overview-list__list-item')
        for product in products:
            clean = product.get_text().split('\n')
            clean = list(filter(None, clean))
            if len(clean) > 1:
                name = clean[0] + " " + re.sub(r'\t', '', clean[1])
                index = clean.index("Към предложението")
                price = float(re.sub(r'\s', '', clean[index - 2]).replace(',', '.'))
                pr, _ = Product.objects.get_or_create(name=name, price=price, promotion=promotion)
    return True


def lidl(self):
    response = requests.get(lidl_cats[0])
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", "product product--tile")
    expires = f"{soup.find('div', 'ribbon__text').get_text().split()[-1]}{datetime.datetime.now().year}"
    promotion, _ = Promotion.objects.get_or_create(store=self, expires=datetime.datetime.strptime(expires, '%d.%m.%Y'))
    for product in products:
        clean = product.get_text().split('\n')
        clean = list(filter(None, clean))
        pr, _ = Product.objects.get_or_create(name=clean[0].strip(), price=float(clean[4].strip().replace(',', '.')),
                                              promotion=promotion)
