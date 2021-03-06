from django.db import models

from hospitals.models import Department, Hospital


class Category(models.Model):
    category_name = models.CharField(max_length=50,
                                     verbose_name='Category title')
    hospital = models.ForeignKey(Hospital, related_name='categories',
                                 on_delete=models.CASCADE,
                                 verbose_name='Hospital')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']

    def __str__(self):
        return f"{self.category_name}"


class Item(models.Model):
    name = models.CharField(max_length=120,
                            verbose_name='Item title',
                            unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Category', unique=False)
    hospital = models.ForeignKey(Hospital, related_name='items',
                                 on_delete=models.CASCADE,
                                 verbose_name='Hospital')
    description = models.CharField(max_length=250,
                                   verbose_name='Item description',
                                   default='', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Quantity')
    price_of_one = models.DecimalField(default=1,
                                       verbose_name='Item price USD',
                                       decimal_places=2,
                                       max_digits=6, blank=True, null=True)
    price = models.DecimalField(default=1,
                                verbose_name='Full price',
                                decimal_places=2,
                                max_digits=6,
                                editable=False,
                                blank=True, null=True)

    @property
    def full_price(self):
        if self.price_of_one:
            price = self.quantity * self.price_of_one
            return price
        return 0

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}"
