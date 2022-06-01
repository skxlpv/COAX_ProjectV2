from django.db import models
from django.utils.translation import gettext_lazy as _


class Cities(models.Model):
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.city}, {self.region}"

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Departments(models.Model):
    department_name = models.CharField(max_length=255, unique=True, default='')

    def __str__(self):
        return f"{self.department_name}"

    class Meta:
        verbose_name = _('Departament')
        verbose_name_plural = _('Departments')


class Hospitals(models.Model):
    hospital_name = models.CharField(max_length=255, unique=True, verbose_name='Hospital name')
    hospital_city = models.ForeignKey(Cities, on_delete=models.CASCADE,
                                      related_name='cities', default='',
                                      verbose_name='City')
    hospital_departments = models.ManyToManyField(Departments, verbose_name='Departments')

    def __str__(self):
        return f"{self.hospital_name}"

    class Meta:
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitals')
