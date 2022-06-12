from mixer.backend.django import mixer
from rest_framework import status

from api.tests import BaseAPITest
from hospitals.models import Department, Hospital
from management.models import Item, Category


class TestItemViewSet(BaseAPITest):

    def setUp(self):
        self.department = mixer.blend(Department)
        self.hospital = mixer.blend(Hospital)

        self.item = mixer.blend(Item)
        self.category = mixer.blend(Category)

        self.user = self.create_user_and_login()

        self.patch_data = {
            "id": 2,
            "category_name": 2,
            "name": "MAniitorRr",
            "description": "asopdiasopdi",
            "quantity": 15,
            "price_of_one": "40.00"
        }

        self.invalid_patch_data = {
            "id": 2,
            "category_name": 2,
            "name": "MAniitorRr",
            "description": "asopdiasopdi",
            # NO QUANTITY,
            "price_of_one": "40.00"
        }

        self.item_data = {
            "category_name": 1,
            "name": "Some Reanimation Item",
            "description": "Some Description",
            "quantity": 3000,
            "price_of_one": "14.00"
        }

    def test_list_items_GET(self):
        resp = self.client.get('/v1/management/items/', )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_detail_item_GET(self):
        resp = self.client.get('/v1/management/items/1/', )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_item_POST(self):
        resp = self.client.post('/v1/management/items/', self.item_data)
        self.assertEqual(resp.status_code, 201)

    def test_create_item_no_required_data_POST(self):
        resp = self.client.post('/v1/management/items/', self.item_data)
        self.assertEqual(resp.status_code, 400)

    def test_update_item_PATCH(self):
        resp = self.client.patch('/v1/management/items/1/', data=self.patch_data)

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['quantity'], self.patch_data['quantity'])

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, self.patch_data['quantity'])

    def test_update_validation_error_PATCH(self):
        self.patch_data['quantity'] = None
        resp = self.client.patch('/v1/management/items/1/', data=self.invalid_patch_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_methods_when_unauthenticated(self):
        self.logout()

        resp = self.client.get('/v1/management/items/')
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get('/v1/management/items/1/')
        self.assertEqual(resp.status_code, 403)

        resp = self.client.patch('/v1/management/items/1/', data=self.patch_data)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get('/v1/management/categories/')
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get('/v1/management/categories/1/')
        self.assertEqual(resp.status_code, 403)

#############################################################

    def test_list_category_GET(self):
        resp = self.client.get('/v1/management/categories/')
        self.assertEqual(resp.status_code, 200)

    def test_detail_category_GET(self):
        resp = self.client.get('/v1/management/categories/1/')
        self.assertEqual(resp.status_code, 200)

