from django.contrib import admin

# Register your models here.
from patients.models import Patient

admin.site.register(Patient)