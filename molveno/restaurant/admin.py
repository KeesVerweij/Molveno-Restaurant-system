from django.contrib import admin
from django.contrib import auth
from .models import Inventory, MenuItem, Ingredient, MenuItemType, CourseType

# Register your models here.


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'brand', 'supplier', 'article_number',
                    'unit', 'container_amount', 'price', 'unit_price',
                    'minimum_quantity', 'current_stock', 'stock_value',
                    'order_quantity')


class MenuItemAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)


admin.site.register(Inventory, InventoryAdmin)
admin.site.register(MenuItemType)
admin.site.register(CourseType)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
