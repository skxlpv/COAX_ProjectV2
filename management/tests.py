from mixer.backend.django import mixer
from rest_framework import status

from api.tests import BaseAPITest
from hospitals.models import Department, Hospital
from management.models import Item


class TestItemViewSet(BaseAPITest):

    def setUp(self):
        self.department = mixer.blend(Department)
        self.hospital = mixer.blend(Hospital)
        self.item = mixer.blend(Item)

        self.user = self.create_user_and_login()

        self.patch_data = {
            "id": 2,
            "category_name": 2,
            "name": "MAniitorRr",
            "description": "asopdiasopdi",
            "quantity": 15,
            "price_of_one": "40.00"
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
        resp = self.client.patch('/v1/management/items/1/', data=self.patch_data)

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['quantity'], self.patch_data['quantity'])

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, self.patch_data['quantity'])
