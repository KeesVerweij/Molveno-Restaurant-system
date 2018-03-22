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

    container_amount = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    order_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.description
