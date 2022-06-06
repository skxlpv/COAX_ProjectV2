from django.contrib import admin
from .models import City, Hospital, Department


class Admin(admin.ModelAdmin):
    filter_horizontal = ['hospital_departments']


admin.site.register(City)
admin.site.register(Hospital, Admin)
admin.site.register(Department)
