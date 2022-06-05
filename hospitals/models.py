from django.db import models
from django.utils.translation import gettext_lazy as _


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

    def __str__(self):
        return f"{self.hospital_name}"

    class Meta:
        ordering = ('-hospital_name', )
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitals')


class City(models.Model):
    city_name = models.CharField(max_length=255)
    region_name = models.CharField(max_length=255)
    hospital_name = models.ForeignKey(Hospital, related_name='hospital', on_delete=models.CASCADE, default=1)
    #hospital_departments = models.ManyToManyField(Department, related_name='city_departments')
    # department_name = models.ForeignKey(Department, related_name='city_department',
    #                                     on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.city_name}, {self.region_name}"

    class Meta:
        ordering = ('-region_name', )
        verbose_name = _('City')
        verbose_name_plural = _('Cities')