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
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.department_name}"

    class Meta:
        ordering = ('-department_name',)
        verbose_name = _('Departament')
        verbose_name_plural = _('Departments')


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=255)
    hospital_departments = models.ManyToManyField(Department, related_name='departments')
    region = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hospital_name} | {self.region}"

    class Meta:
        ordering = ('-region', 'hospital_name')
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitals')
