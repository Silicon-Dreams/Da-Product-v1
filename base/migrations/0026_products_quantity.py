# Generated by Django 4.1.7 on 2023-03-15 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_alter_products_fordisplay'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
