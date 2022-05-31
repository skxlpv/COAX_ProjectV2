from django.contrib import admin
from .models import Cities, Hospitals, Departments


class Admin(admin.ModelAdmin):
    filter_horizontal = ['hospital_departments']


admin.site.register(Cities)
admin.site.register(Hospitals, Admin)
admin.site.register(Departments)