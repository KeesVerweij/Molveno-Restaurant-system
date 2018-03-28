from django.db import models

class Inventory(models.Model):
    description = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
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
    unit_price = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    minimum_quantity = models.DecimalField(
        default=0, max_digits=5, decimal_places=2
    )
    current_stock = models.DecimalField(
        default=0, max_digits=5, decimal_places=2
    )
    stock_value = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )
    order_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.description + ', ' + self.unit

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
    description = models.CharField(max_length=2000)
    menu_item_type = models.ForeignKey('MenuItemType',
                                       on_delete=models.PROTECT)
    course_type = models.ForeignKey('CourseType',
                                    on_delete=models.PROTECT)
    recipe = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.menu_item)
