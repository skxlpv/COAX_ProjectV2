from django.contrib import admin

from hospitals.models import Departments
from management.models import Category, Item

admin.site.register(Category)
admin.site.register(Item)
