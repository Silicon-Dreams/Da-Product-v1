# Generated by Django 4.1.7 on 2023-03-07 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_alter_multipleimage_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="filterField",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
