# Generated by Django 4.1.7 on 2023-03-11 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0015_additionaluserinfo_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionaluserinfo",
            name="image",
            field=models.ImageField(
                blank=True, default="defaultImg.png", null=True, upload_to=""
            ),
        ),
    ]
