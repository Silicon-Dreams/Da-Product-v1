# Generated by Django 4.1.7 on 2023-03-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0013_additionaluserinfo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionaluserinfo",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="additionaluserinfo",
            name="phoneNumber",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
