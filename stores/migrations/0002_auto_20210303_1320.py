# Generated by Django 3.1.4 on 2021-03-03 13:20

from django.db import migrations


def make_objects(apps, schema_editor):
    Store = apps.get_model("stores", "Store")
    new_store = Store(name="Billa")
    new_store.save()

    new_store = Store(name="Kaufland")
    new_store.save()

    new_store = Store(name="Lidl")
    new_store.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [migrations.RunPython(make_objects)]
