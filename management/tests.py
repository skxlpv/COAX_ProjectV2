from mixer.backend.django import mixer

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

    def test_list(self):
        resp = self.client.get('/v1/management/items/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'], Item.objects.all().count())

    def test_detail(self):
        resp = self.client.get(f'/v1/management/items/{self.item.id}/', )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['id'], self.item.id)
        self.assertTrue(len(resp.data), 1)

    def test_create(self):
        self.item_data = {
            "category_name": self.category.id,
            "name": "Some Reanimation Item",
            "description": "Some Description",
            "quantity": 3000,
            "price_of_one": "14.00"
        }

        resp = self.client.post('/v1/management/items/', data=self.item_data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data['name'], self.item_data['name'])
        self.assertTrue(resp.data['category_name'], self.item_data['category_name'])


    def test_create_no_required_data(self):
        self.invalid_item_data = {
            "name": "Some Reanimation Item",
            "description": "Some Description",
            "price_of_one": "14.00"
        }

        resp = self.client.post('/v1/management/items/', self.invalid_item_data)

        self.assertEqual(resp.status_code, 400)
        self.assertNotEquals(resp.data, self.invalid_item_data)

    def test_partial_update(self):
        self.patch_data = {
            "quantity": 15,
        }

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.patch_data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['quantity'], self.patch_data['quantity'])

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, self.patch_data['quantity'])

    def test_partial_update_validation_error(self):
        self.invalid_patch_data = {
            # NO QUANTITY
        }

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.invalid_patch_data)

        self.assertEqual(resp.status_code, 400)

    def test_default_after_patch(self):
        self.invalid_patch_data = {
            # NO QUANTITY
        }

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.invalid_patch_data)

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 1)

    def test_methods_when_unauthenticated(self):
        self.patch_data = {
            "quantity": 15,
        }

        self.logout()

        resp = self.client.get('/v1/management/items/')
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get(f'/v1/management/items/{self.item.id}/')
        self.assertEqual(resp.status_code, 401)

        resp = self.client.patch(f'/v1/management/items/{self.item.id}/', data=self.patch_data)
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get('/v1/management/categories/')
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get(f'/v1/management/categories/{self.item.id}/')
        self.assertEqual(resp.status_code, 401)


#############################################################

class TestCategoryViewSet(BaseAPITest):

    def setUp(self):
        self.department = mixer.blend(Department)

        self.category = mixer.blend(Category, department=self.department)
        self.item = mixer.blend(Item, category_name=self.category)
        self.category.items.set([self.item])

        self.user = self.create_and_login()

    def test_list(self):
        resp = self.client.get('/v1/management/categories/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data['results']), Item.objects.all().count())

    def test_detail(self):
        resp = self.client.get(f'/v1/management/categories/{self.category.id}/')
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['id'], self.item.id)
        self.assertTrue(len(resp.data), 1)
