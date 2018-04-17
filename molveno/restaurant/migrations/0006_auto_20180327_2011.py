# Generated by Django 2.0.2 on 2018-03-27 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20180327_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredientamount',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='ingredientamount',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='inventory',
            name='article_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory',
            name='brand',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='container_amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='current_stock',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='inventory',
            name='minimum_quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='inventory',
            name='order_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='stock_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='inventory',
            name='supplier',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='unit',
            field=models.CharField(choices=[('KG', 'Kilogram'), ('PCS', 'Pieces'), ('LTR', 'Liter')], default='KG', max_length=200),
        ),
        migrations.AddField(
            model_name='inventory',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.DeleteModel(
            name='IngredientAmount',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Inventory'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.MenuItem'),
        ),
    ]