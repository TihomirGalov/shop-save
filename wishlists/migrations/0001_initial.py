# Generated by Django 3.1.4 on 2021-03-10 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20210304_1850'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('user', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=1, max_digits=9, verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to='products.product', verbose_name='Product')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='wishlists.wishlist', verbose_name='Wishlist')),
            ],
            options={
                'verbose_name': 'Wishlist Item',
                'verbose_name_plural': 'Wishlists Items',
            },
        ),
    ]
