# Generated by Django 2.0.2 on 2018-04-05 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0022_auto_20180405_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='_stock_value',
        ),
    ]
