from django.test import TestCase
from .models import Store


class StoresTestCase(TestCase):

    def test_all_stores_are_available(self):
        names = {'Billa', 'Lidl', 'Kaufland'}
        for store in Store.objects.all():
            self.assertIn(store.name, names, f"The store {store.pk} is not supported or a store is repeated")
            names.remove(store.name)
