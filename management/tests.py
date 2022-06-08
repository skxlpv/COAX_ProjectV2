from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class TestItemViewSet(APITestCase):

    def setUp(self):
        client = APIClient()

        self.user = User.objects.create_superuser(email='test@test.com', password='1234512345',
                                                  first_name='test', last_name='test')

    def test_list_items(self):
        resp = self.client.post('/v1/api/user/token/',
                                {'email': 'test@test.com', 'password': '1234512345'})

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)

        self.user.is_active = True
        self.user.save()

        token = AccessToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}"
        )
        resp = self.client.get('/v1/management/items/',)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
