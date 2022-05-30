from django.utils.text import slugify
from django.db import models

from hospitals.models import Departments


class Item(models.Model):
    name = models.CharField(max_length=120, verbose_name='Item title')
    category = models.ForeignKey('Category', related_name="items",
                                 on_delete=models.CASCADE,
                                 verbose_name='Belongs to')
    quantity = models.IntegerField(default=1, verbose_name='Quantity of item')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Category title')
    department = models.ForeignKey(Departments, related_name='categories',
                                   on_delete=models.CASCADE,
                                   verbose_name='Department', default=1)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
