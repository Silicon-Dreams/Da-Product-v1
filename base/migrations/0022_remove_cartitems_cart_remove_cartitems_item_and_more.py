# Generated by Django 4.1.7 on 2023-03-12 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0021_cart_cartitems"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitems",
            name="cart",
        ),
        migrations.RemoveField(
            model_name="cartitems",
            name="item",
        ),
        migrations.RemoveField(
            model_name="specialoffer",
            name="product",
        ),
        migrations.RemoveField(
            model_name="products",
            name="forDisplay",
        ),
        migrations.RemoveField(
            model_name="products",
            name="views",
        ),
        migrations.DeleteModel(
            name="Cart",
        ),
        migrations.DeleteModel(
            name="CartItems",
        ),
        migrations.DeleteModel(
            name="SpecialOffer",
        ),
    ]
