# Generated by Django 4.1.7 on 2023-03-18 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0033_onedayoffer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="base.category",
            ),
        ),
    ]
