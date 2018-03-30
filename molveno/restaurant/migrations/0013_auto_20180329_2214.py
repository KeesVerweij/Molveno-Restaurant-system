# Generated by Django 2.0.2 on 2018-03-29 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuAddition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.Menu')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='MenuCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name of menu card')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemAddition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('menu_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.MenuCard')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.MenuItem')),
            ],
            options={
                'verbose_name': 'Menu Item',
                'verbose_name_plural': 'Menu items',
            },
        ),
        migrations.AddField(
            model_name='menuaddition',
            name='menu_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.MenuCard'),
        ),
    ]
