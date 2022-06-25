from django.db import models

from core import settings
from hospitals.models import Hospital
from users.models import User


class Patient(models.Model):
    first_name = models.CharField(default='NO NAME', max_length=50)
    last_name = models.CharField(default='NO LAST NAME', max_length=50)
    phone_number = models.CharField(default='NO PHONE NUMBER', max_length=50)
    email = models.EmailField(default='NO EMAIL', max_length=200, blank=True)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=False)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)
    diagnosis = models.TextField(default='NO DIAGNOSIS', blank=True)
    receipt = models.TextField(default='NO RECEIPT', blank=True)

    is_discharged = models.BooleanField(default=False)

    check_in_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
