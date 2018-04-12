# Generated by Django 2.0.2 on 2018-04-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0017_remove_inventory_stock_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='container_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
