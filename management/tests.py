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

        self.category_data = {
            "category_name": "dopsfoposf",
        }

    # GET list of all the items
    def test_list_items_GET(self):
        resp = self.client.get('/v1/management/items/', )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # GET detailed info about a single item
    def test_detail_item_GET(self):
        resp = self.client.get('/v1/management/items/1/', )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # PATCH item's quantity, no matter what other data was passed
    def test_update_item_PATCH(self):
        # PASS the valid data in the PATCH request
        resp = self.client.patch('/v1/management/items/1/', data=self.patch_data)

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['quantity'], self.patch_data['quantity'])

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, self.patch_data['quantity'])

    # PATCH invalid data without the required 'quantity' field
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
