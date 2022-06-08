from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from mixer.backend.django import mixer

from api.tests import BaseAPITest
from hospitals.models import Department, Hospital
from management.models import Item


class TestItemViewSet(BaseAPITest):

    def setUp(self):
        self.department = mixer.blend(Department)
        self.item = mixer.blend(Item)

        self.user = self.create_and_login()

    def test_list_items_GET(self):
        resp = self.client.get('/v1/management/items/', )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_detail_item_GET(self):
        resp = self.client.get('/v1/management/items/1/', )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
