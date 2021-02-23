# Generated by Django 3.1.4 on 2020-12-06 11:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires', models.DateTimeField(default=datetime.datetime(2020, 12, 6, 11, 8, 1, 547940))),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='stores.store')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('description', models.TextField(blank=True, null=True)),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.promotion')),
            ],
        ),
    ]