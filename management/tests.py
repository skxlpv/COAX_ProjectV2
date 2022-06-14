from mixer.backend.django import mixer
from rest_framework import status

from api.tests import BaseAPITest
from hospitals.models import Department, Hospital, City
from management.models import Item, Category


class TestItemViewSet(BaseAPITest):

    def setUp(self):
        self.department1 = mixer.blend(Department)
        self.department2 = mixer.blend(Department)
        self.city = mixer.blend(City)
        self.hospital = mixer.blend(Hospital)
        self.hospital.hospital_departments.set([self.department1.pk, self.department2.pk])

        self.category = mixer.blend(Category, department=self.department2)
        self.item = mixer.blend(Item, category_name=self.category)
        self.category.items.set([self.item])

        self.user = self.create_and_login()

        self.item_data = {
            "category_name": 1,
            "name": "Some Reanimation Item",
            "description": "Some Description",
            "quantity": 3000,
            "price_of_one": "14.00"
        }

    def test_list_items_GET(self):
        resp = self.client.get('/v1/management/items/', )

        self.assertEqual(resp.status_code, 200)

        data = resp.content.decode('utf-8')
        self.assertTrue(data, self.item.name)  # test if such item is in a response

    def test_detail_item_GET(self):
        resp = self.client.get(f'/v1/management/items/{self.item.id}/', )

        self.assertEqual(resp.status_code, 200)

        data = resp.content.decode('utf-8')
        self.assertTrue(data, self.item.id)  # test if item with such ID is in a response

    def test_create_item_POST(self):
        resp = self.client.post('/v1/management/items/', self.item_data)
        self.assertEqual(resp.status_code, 201)

        data = resp.content.decode('utf-8')
        self.assertTrue(data, self.item_data)  # test if the response data is the same with the request data

    def test_create_item_no_required_data_POST(self):
        self.invalid_item_data = {
            "name": "Some Reanimation Item",
            "description": "Some Description",
            "price_of_one": "14.00"
        }

        resp = self.client.post('/v1/management/items/', self.invalid_item_data)
        self.assertEqual(resp.status_code, 400)

    def test_update_item_PATCH(self):
        self.patch_data = {
            "quantity": 15,
        }

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.patch_data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['quantity'], self.patch_data['quantity'])

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, self.patch_data['quantity'])

    def test_update_validation_error_PATCH(self):
        self.invalid_patch_data = {
            # NO QUANTITY
        }

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.invalid_patch_data)

        self.assertEqual(resp.status_code, 400)  # test if validation fails

    def test_default_after_patch(self):
        self.invalid_patch_data = {
            # NO QUANTITY
        }

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.invalid_patch_data)

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 1)  # test if the current item's quantity of the patched item
        # is equal to the Item's default field (should be 1)

    def test_methods_when_unauthenticated(self):
        self.patch_data = {
            "quantity": 15,
        }

        self.logout()

        resp = self.client.get('/v1/management/items/')
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(f'/v1/management/items/{self.item.id}/')
        self.assertEqual(resp.status_code, 403)

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.patch_data)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get('/v1/management/categories/')
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(f'/v1/management/categories/{self.item.id}/')
        self.assertEqual(resp.status_code, 403)


#############################################################

class TestCategoryViewSet(BaseAPITest):

    def setUp(self):
        self.department = mixer.blend(Department)

        self.category = mixer.blend(Category, department=self.department)
        self.item = mixer.blend(Item, category_name=self.category)
        self.category.items.set([self.item])

        self.user = self.create_and_login()

    def test_list_category_GET(self):
        resp = self.client.get('/v1/management/categories/')
        self.assertEqual(resp.status_code, 200)

        data = resp.content.decode('utf-8')
        self.assertTrue(data, self.category.category_name)

    def test_detail_category_GET(self):
        resp = self.client.get(f'/v1/management/categories/{self.category.id}/')
        self.assertEqual(resp.status_code, 200)

        data = resp.content.decode('utf-8')
        self.assertTrue(data, self.item.id)
