# Generated by Django 4.1.7 on 2023-03-05 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_products_multipleimage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="multipleimage",
            options={"verbose_name_plural": "Multiple Image"},
        ),
        migrations.AlterModelOptions(
            name="products",
            options={"verbose_name_plural": "Products"},
        ),
    ]