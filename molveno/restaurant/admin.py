from django.contrib import admin, auth
from .models import Inventory
from .models import MenuItem
from .models import Ingredient
from .models import MenuItemType
from .models import CourseType
from .models import Supplier
from .models import Menu
from .models import MenuCard
from .models import MenuAddition
from .models import MenuItemAddition


class MenuItemAdditionInline(admin.TabularInline):
    model = MenuItemAddition
    extra = 0


class MenuAdditionInline(admin.TabularInline):
    model = MenuAddition
    extra = 0


class MenuCardAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (MenuItemAdditionInline, MenuAdditionInline,)


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'brand', 'supplier', 'article_number',
                    'unit', 'container_amount', 'price', 'unit_price',
                    'minimum_quantity', 'current_stock', 'stock_value',
                    'order_quantity')
    ordering = ['description']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_type', 'menu_item_type')
    inlines = (IngredientInline,)
    ordering = ['name']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address_line1', 'address_line2', 'phone', 'email_address')
    ordering = ['name']

class MenuInline(admin.TabularInline):
    model = Menu.menu_items.through
    extra = 0

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('menu_items',)
    inlines = (MenuInline,)


admin.site.register(MenuCard, MenuCardAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(MenuItemType)
admin.site.register(CourseType)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
