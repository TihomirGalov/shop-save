# Generated by Django 3.1.4 on 2021-03-04 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210304_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 4, 19, 12, 55, 716661), verbose_name='Expires'),
        ),
    ]
