# Generated by Django 2.0.2 on 2018-04-04 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_auto_20180329_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='unit_price',
        ),
    ]
