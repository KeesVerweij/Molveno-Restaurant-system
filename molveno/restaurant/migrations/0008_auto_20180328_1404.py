# Generated by Django 2.0.2 on 2018-03-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_auto_20180328_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name': 'Inventory Item', 'verbose_name_plural': 'Inventory'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
