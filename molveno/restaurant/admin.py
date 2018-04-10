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
from .models import Order


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
    readonly_fields = ('unit_price', 'stock_value')
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
    # pass


def complete_order(modeladmin, request, queryset):
    """
    function used in the Order Admin page to add a custom action to complete orders
    """
    queryset.update(completed=True)


# provide a verbose desciption for the complete orders function
complete_order.short_description = "mark orders as completed"


def uncomplete_order(modeladmin, request, queryset):
    """
    function used in the Order Admin page to add a custom action to complete orders
    """
    queryset.update(completed=False)


# provide a verbose desciption for the complete orders function
uncomplete_order.short_description = "mark orders as not completed"


class OrderAdmin(admin.ModelAdmin):
    # changes to the Orders overview page
    list_display = ('menu_item', 'table_no', 'completed')
    # show custom action to complete orders
    actions = [complete_order, uncomplete_order]

    # def get_actions(self, request):
    #     """
    #     remove delete action
    #     """
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    # remove add functionality
    def has_add_permission(self, request):
        """
        Remove the add button
        """
        return False

    def get_list_display_links(self, request, list_display):
        """
        Override Django's default implementation to specify no links unless
        these are explicitly set.
        """
        if self.list_display_links or not list_display:
            return self.list_display_links
        else:
            return (None,)


admin.site.register(MenuCard, MenuCardAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(MenuItemType)
admin.site.register(CourseType)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
