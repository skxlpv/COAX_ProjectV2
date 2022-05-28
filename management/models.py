from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


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


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Category title')
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children',
                               verbose_name='Is subcategory of')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
