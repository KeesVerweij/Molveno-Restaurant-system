# Generated by Django 2.0.2 on 2018-03-28 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_auto_20180327_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item_type', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='diet_type',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.Inventory'),
        ),
        migrations.DeleteModel(
            name='DietType',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menu_item_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='restaurant.MenuItemType'),
            preserve_default=False,
        ),
    ]