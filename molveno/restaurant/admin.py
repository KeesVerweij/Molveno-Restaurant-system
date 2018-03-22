from django.contrib import admin

from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'brand', 'supplier', 'article_number',
                    'unit', 'container_amount', 'price', 'unit_price',
                    'minimum_quantity', 'current_stock', 'order_quantity')


admin.site.register(Inventory, InventoryAdmin)
