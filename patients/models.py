from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from hospitals.models import Hospital
from users.models import User


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(default='', unique=True, blank=True)
    email = models.EmailField(max_length=200, null=True, unique=True)

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor', default=0)
    diagnosis = models.TextField(blank=True)
    receipt = models.TextField(blank=True)

    is_discharged = models.BooleanField(default=False)

    check_in_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-id']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
