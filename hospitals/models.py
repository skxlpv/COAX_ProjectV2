from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.city}, {self.region}"

    class Meta:
        ordering = ('-region',)
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ('-name',)
        verbose_name = _('Departament')
        verbose_name_plural = _('Departments')


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    hospital_departments = models.ManyToManyField(Department, related_name='hospital_deps')
    region = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.region}"

    class Meta:
        ordering = ('-region', 'name')
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitals')
