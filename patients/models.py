from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from hospitals.models import Hospital
from users.models import User


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(default='', unique=True, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, unique=True)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
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