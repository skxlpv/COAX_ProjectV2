from django.db import models
from django.utils.translation import gettext_lazy as _


class Cities(models.Model):
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.city}, {self.region}"

    class Meta:
        ordering = ('-region', )
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Hospitals(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Cities, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.region.city}"

    class Meta:
        ordering = ('-region', )
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitals')


class Departments(models.Model):
    name = models.CharField(max_length=255)
    hospital_name = models.ForeignKey(Hospitals, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.hospital_name}"

    class Meta:
        ordering = ('-name',)
        verbose_name = _('Departament')
        verbose_name_plural = _('Departments')