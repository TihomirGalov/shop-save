# Generated by Django 3.1.4 on 2021-03-04 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20210303_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'verbose_name': 'Store', 'verbose_name_plural': 'Stores'},
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
