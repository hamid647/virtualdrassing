# Generated by Django 4.1.1 on 2023-05-04 19:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_buyer_info_quantity_buyer_info_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer_info',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='buyer_info',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 5, 0, 51, 41, 188045), editable=False),
        ),
        migrations.AlterField(
            model_name='buyer_info',
            name='total_price',
            field=models.IntegerField(),
        ),
    ]
