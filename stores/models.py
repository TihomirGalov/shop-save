from django.db import models
from .scraper import kaufland, billa, lidl


class Store(models.Model):
    name = models.CharField(max_length=255)

    def get_data(self):
        if self.name == "Billa":
            billa(self)
        if self.name == "Kaufland":
            kaufland(self)
        if self.name == "Lidl":
            lidl(self)

    def __str__(self):
        return self.name


