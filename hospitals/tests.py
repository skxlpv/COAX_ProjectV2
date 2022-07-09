from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.tests import BaseAPITest
from hospitals.models import Hospital, City, Department


class TestHospitalViewSet(BaseAPITest):
    def setUp(self):
        self.user = self.create_and_login()
        self.single_object = 1

    def test_list(self):
        self.hospital1 = mixer.blend(Hospital)
        self.hospital2 = mixer.blend(Hospital)
        self.hospital3 = mixer.blend(Hospital)

        resp = self.client.get('/v1/hospitals/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'], Hospital.objects.all().count())

    def test_detail(self):
        self.hospital = mixer.blend(Hospital)

        resp = self.client.get(f'/v1/hospitals/{self.hospital.id}/')

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['id'], self.hospital.id)
        self.assertTrue(len(resp.data), self.single_object)


class TestCityViewSet(BaseAPITest):
    def setUp(self):
        self.user = self.create_and_login()
        self.single_object = 1

    def test_list(self):
        self.city1 = mixer.blend(City)
        self.city2 = mixer.blend(City)
        self.city3 = mixer.blend(City)

        resp = self.client.get('/v1/hospitals/city/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'], City.objects.all().count())

    def test_detail(self):
        self.city = mixer.blend(City)

        resp = self.client.get(f'/v1/hospitals/city/{self.city.id}/')

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['id'], self.city.id)
        self.assertTrue(len(resp.data), self.single_object)


class TestDepartmentViewSet(BaseAPITest):
    def setUp(self):
        self.user = self.create_and_login()
        self.single_object = 1

    def test_list(self):
        self.department1 = mixer.blend(Department)
        self.department2 = mixer.blend(Department)
        self.department3 = mixer.blend(Department)

        resp = self.client.get('/v1/hospitals/department/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'], Department.objects.all().count())

    def test_detail(self):
        self.department = mixer.blend(Department)

        resp = self.client.get(f'/v1/hospitals/department/{self.department.id}/')

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['id'], self.department.id)
        self.assertTrue(len(resp.data), self.single_object)
