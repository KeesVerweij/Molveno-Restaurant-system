import datetime
from django.db import models
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class Inventory(models.Model):
    description = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    supplier = models.ForeignKey("Supplier", on_delete=models.PROTECT)
    article_number = models.IntegerField(default=0)

    UNIT_CHOICES = (
        ('KG', 'Kilogram'),
        ('PCS', 'Pieces'),
        ('LTR', 'Liter'),
    )

    unit = models.CharField(
        max_length=200,
        choices=UNIT_CHOICES,
        default='KG'
    )

    container_amount = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    price = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    minimum_quantity = models.DecimalField(
        default=0, max_digits=5, decimal_places=2
    )
    current_stock = models.DecimalField(
        default=0, max_digits=5, decimal_places=2
    )
    order_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    def _get_unit_price(self):
        if self.price and self.container_amount:
            return round((self.price / self.container_amount), 2)
    unit_price = property(_get_unit_price)

    def _get_stock_value(self):
        if self.current_stock and self.price and self.container_amount:
            return round((self.current_stock * (self.price / self.container_amount)), 2)
    stock_value = property(_get_stock_value)

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory"



class MenuItemType(models.Model):
    menu_item_type = models.CharField(max_length=200)

    def __str__(self):
        return self.menu_item_type


class CourseType(models.Model):
    course_type = models.CharField(max_length=200)

    def __str__(self):
        return self.course_type


class MenuItem(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2000, blank = True)
    menu_item_type = models.ForeignKey('MenuItemType',
                                       on_delete=models.PROTECT)
    course_type = models.ForeignKey('CourseType',
                                    on_delete=models.PROTECT)
    recipe = models.TextField(blank = True)

    def __str__(self):
        return self.name + ' (' + str(self.course_type) + '), Suggested selling price: €' + str(self.suggested_selling_price) + ')'

    def _get_uplift(self):
        if self.course_type.course_type == 'Drink':
            value = 1.90
        else:
            value = 1.65
        return value
    uplift = property(_get_uplift)

    def _get_suggested_selling_price(self):
        r = 0
        allingredients = Ingredient.objects.filter(menu_item__in=MenuItem.objects.filter(name = self.name))
        for item in allingredients:
            if item.unit == 'KG' or item.unit == 'L' or item.unit == 'PCS':
                r += ((item.ingredient.price / item.ingredient.container_amount) * item.amount)
            if item.unit == 'G' or item.unit == 'ML':
                r += ((item.ingredient.price / item.ingredient.container_amount) * item.amount/1000)
            else:
                r += ((item.ingredient.price / item.ingredient.container_amount) * item.amount/1000000)
        return round(Decimal((float(r)*self.uplift)),2)
    suggested_selling_price = property(_get_suggested_selling_price)


class Ingredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Inventory, on_delete=models.PROTECT)

    UNIT_CHOICES = (
        ('MG', 'Milligram'),
        ('G', 'Gram'),
        ('KG', 'Kilogram'),
        ('ML', 'Milliliter'),
        ('L', 'Liter'),
        ('PCS', 'Pieces'),
    )

    unit = models.CharField(
        max_length=200,
        choices=UNIT_CHOICES,
        default='G'
    )

    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.menu_item.name

    # def _get_amount_price(self):
    #     if self.amount:
    #         r = round(((self.ingredient.price / self.ingredient.container_amount) * self.amount), 2)
    #         return r
    # amount_price = property(_get_amount_price)


class Supplier(models.Model):
    name = models.CharField("Supplier Name", max_length=200)
    address_line1 = models.CharField("Address Line", max_length=200)
    address_line2 = models.CharField("Address Line", max_length=200)
    phone = models.CharField("Phone Number", max_length=10)
    email_address = models.CharField("Email Address", max_length=100, blank = True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=128)
    menu_items = models.ManyToManyField(MenuItem)

    def _get_suggested_selling_price(self):
        r = 0
        for item in self.menu_items.all():
            r += item.suggested_selling_price
        return round(Decimal(r),2)
    suggested_selling_price = property(_get_suggested_selling_price)

    def __str__(self):
        return self.name + ' (Suggested selling price: €' + str(self.suggested_selling_price) + ')'


class MenuCard(models.Model):
    name = models.CharField("Name of menu card", max_length=100)

    def __str__(self):
        return self.name


class MenuItemAddition(models.Model):
    menu_card = models.ForeignKey(MenuCard, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    #suggested_selling_price = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False)
    selling_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.menu_item.name) + ' (' + str(self.menu_item.course_type) + ") on " + str(self.menu_card) + " for €" + str(self.selling_price)

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu items'

# @receiver(pre_save, sender='MenuItemAddition')
# def show_suggested_price(sender, **kwargs):



class MenuAddition(models.Model):
    menu_card = models.ForeignKey(MenuCard, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    #suggested_selling_price = models.DecimalField(max_digits=5, decimal_places=2, default-0, editable=False)
    selling_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.menu.name) + " on " + str(self.menu_card) + " for €" + str(self.selling_price)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'


class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    table_no = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    completed = models.BooleanField(default=False)
    order_time = models.DateTimeField()
    completed_time = models.DateTimeField()
    remarks = models.CharField('Remarks', max_length=254)

    # Order items shouldn't be deleted in the admin page,
    # we can delete the complete items automatically when payment is processed.

    def __str__(self):
        return str(self.menu_item.name)
