from django.test import TestCase

from .models import Promotion, Product


class PromotionTestCase(TestCase):

    def promotion_items(self):
        for promotion in Promotion.objects.all():
            self.assertNotEqual(promotion.items.all().count(), 0,
                                f"The promotion with id {promotion.pk} is  without products in it")


class ProductTestCase(TestCase):

    def product_price(self):
        self.assertNotEqual(Product.objects.filter(preice__lte=0), 0, "The price of a product  is negative")
