from django.contrib import admin

from events.models import Event


class Admin(admin.ModelAdmin):
    filter_horizontal = ['participants']


admin.site.register(Event, Admin)
