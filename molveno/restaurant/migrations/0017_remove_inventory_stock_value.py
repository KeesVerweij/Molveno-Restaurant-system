# Generated by Django 2.0.2 on 2018-04-04 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0016_remove_inventory_unit_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='stock_value',
        ),
    ]
