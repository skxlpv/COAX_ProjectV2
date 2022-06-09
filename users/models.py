from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.conf import settings
from hospitals.models import Hospital
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name, hospital_name, role, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            hospital_name=hospital_name,
            role=role,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **other_fields  # had to add other field in order to setup user for the tests
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
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=True, null=True)

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
    is_writer = models.BooleanField(default=True)  # NEW
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def __str__(self):
        return self.email
