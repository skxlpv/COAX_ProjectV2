from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer
from rest_framework.test import APITestCase

# Create your tests here.
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from hospitals.models import Hospital, City
from users.models import User


class BaseAPITest(APITestCase):

    # def create_hospital(self, hospital_name='Test hospital', region=1):
    #     hospital = Hospital.objects.create(hospital_name=hospital_name, region_id=region,)
    #     return hospital

    def create(self, email='test@mail.com', password='test_password',
               first_name='test', last_name='test', hospital=None, is_writer=False,):
        user = User.objects.create_user(email=email, password=password,
                                        first_name=first_name, last_name=last_name, hospital=hospital)
        user.last_login = timezone.now()
        user.is_active = True
        user.is_writer = is_writer
        user.save()
        return user

    def create_super_user(self, email='super-test@test.com', password='1234512345',
                          first_name='test', last_name='test', is_writer=False):
        user = User.objects.create_superuser(email=email, password=password,
                                             first_name=first_name, last_name=last_name)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()
        user.is_writer = is_writer
        return user

    def create_and_login(self, email='test@test.com', password='1234512345qq',
                         first_name='test', last_name='test', hospital=None, is_writer=False,):
        user = self.create(email=email, password=password,
                           first_name=first_name, last_name=last_name, hospital=hospital, is_writer=is_writer)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )
