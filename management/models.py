from django.db import models

from hospitals.models import Department


class Category(models.Model):
    category_name = models.CharField(max_length=50,
                                     unique=True,
                                     verbose_name='Category title')
    department = models.ForeignKey(Department, related_name='categories',
                                   on_delete=models.CASCADE, default=1,
                                   verbose_name='Department')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.category_name}"


class Item(models.Model):
    name = models.CharField(max_length=120,
                            verbose_name='Item title',
                            unique=True)
    category_name = models.ForeignKey(Category, related_name="items",
                                      on_delete=models.CASCADE,
                                      verbose_name='Belongs to')
    description = models.CharField(max_length=250,
                                   verbose_name='Item description',
                                   default='', null=True)
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Quantity')
    price_of_one = models.DecimalField(default=1,
                                       verbose_name='Item price USD',
                                       decimal_places=2,
                                       max_digits=6)
    price = models.DecimalField(default=1,
                                verbose_name='Full price',
                                decimal_places=2,
                                max_digits=6,
                                editable=False)

    @property
    def full_price(self):
        price = self.quantity * self.price_of_one
        return price

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.name}"
