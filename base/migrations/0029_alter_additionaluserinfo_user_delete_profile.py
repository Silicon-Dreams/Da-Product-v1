# Generated by Django 4.1.7 on 2023-03-17 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0028_alter_additionaluserinfo_user_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionaluserinfo",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prof",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
