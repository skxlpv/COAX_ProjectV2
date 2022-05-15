from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.conf import settings
from hospitals.models import Hospitals


class CustomUsermanager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name, hospital_name, role):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            hospital_name=hospital_name,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    hospital = models.ForeignKey(Hospitals, on_delete=models.CASCADE, blank=True, null=True)

    LEADER = "LD"
    HELPER = "HP"
    COMMON = "CM"
    ROLE_CHOICES = [
        (LEADER, "Голова"),
        (HELPER, "Помічник"),
        (COMMON, "Дятел")
    ]
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=COMMON,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUsermanager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

