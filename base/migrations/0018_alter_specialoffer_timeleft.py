# Generated by Django 4.1.7 on 2023-03-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0017_specialoffer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="specialoffer",
            name="timeLeft",
            field=models.DateField(),
        ),
    ]
