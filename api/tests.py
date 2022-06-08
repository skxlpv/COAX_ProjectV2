from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase

# Create your tests here.
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class BaseAPITest(APITestCase):

    def create_super_user(self, email='test@test.com', password='1234512345',
                          first_name='test', last_name='test'):
        user = User.objects.create_superuser(email=email, password=password,
                                             first_name=first_name, last_name=last_name)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, email='test@test.com', password='1234512345',
                         first_name='test', last_name='test'):
        user = self.create_super_user(email=email, password=password,
                                      first_name=first_name, last_name=last_name)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )
