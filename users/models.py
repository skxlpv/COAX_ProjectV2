from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.conf import settings
from hospitals.models import Hospital
from django.utils.translation import gettext_lazy as _
from PIL import Image


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            # hospital_name=hospital_name,
            # role=role,
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='media/profile_images')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        width, height = img.size

        if width > 300 and height > 300:
            img.thumbnail((width, height))

        if height < width:
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.image.path)
