# Generated by Django 5.1.2 on 2024-11-06 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wallet_analyzer", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="wallet",
            options={"ordering": ("id",), "verbose_name": "Wallet"},
        ),
    ]