# Generated by Django 5.1.2 on 2024-11-11 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet_analyzer", "0002_alter_wallet_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="address",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]