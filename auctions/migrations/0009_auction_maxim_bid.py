# Generated by Django 3.1.5 on 2021-01-29 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210128_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='maxim_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
