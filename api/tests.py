from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase

# Create your tests here.
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from hospitals.models import Hospital
from users.models import User


class BaseAPITest(APITestCase):

    def create_user(self, email='test@test.com', password='1234512345',
                    first_name='test', last_name='test',
                    hospital=Hospital.objects.get(hospital_name='Hospital'),
                    role='CM', **other_fields):
        user = User.objects.create_superuser(email=email, password=password,
                                             first_name=first_name, last_name=last_name,
                                             hospital=hospital, role=role,
                                             **other_fields)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_user_and_login(self, email='test@test.com', password='1234512345',
                              first_name='test', last_name='test',
                              hospital=Hospital.objects.get(hospital_name='Hospital'),
                              role='CM', **other_fields):
        user = self.create_user(email=email, password=password,
                                first_name=first_name, last_name=last_name,
                                hospital=hospital, role=role,
                                **other_fields)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)