from django.contrib import admin
from django.contrib import auth
from .models import Inventory
from .models import MenuItem
from .models import Ingredient
from .models import MenuItemType
from .models import CourseType
from .models import Menu

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

class MenuInline(admin.TabularInline):
    model = Menu.menu_items.through
    extra = 3

class MenuAdmin(admin.ModelAdmin):
    #list_display = ('name',)
    #exclude = ('menu_items',)
    #inlines = (MenuInline,)
    pass

admin.site.register(Inventory, InventoryAdmin)
admin.site.register(MenuItemType)
admin.site.register(CourseType)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
