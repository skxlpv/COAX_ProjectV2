from mixer.backend.django import mixer
from phonenumber_field.phonenumber import PhoneNumber

from api.tests import BaseAPITest
from hospitals.models import Department, City, Hospital
from patients.models import Patient


class TestPatientViewSet(BaseAPITest):
    def setUp(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLast",
            "diagnosis": "Some Diagnosis",
            "receipt": "Some Receipt",
            "phone_number": "+380957896778"
        }

        self.department = mixer.blend(Department)
        self.city = mixer.blend(City)
        self.hospital = mixer.blend(Hospital)
        self.hospital.hospital_departments.set([self.department.pk])

        self.user = self.create_and_login(hospital=self.hospital)

        self.patient = mixer.blend(Patient, doctor=self.user)

    def test_create(self):
        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data['first_name'], self.patient_data['first_name'])

    def test_list(self):
        resp = self.client.get('/v1/patients/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'], Patient.objects.all().count())

    def test_detail(self):
        resp = self.client.get(f'/v1/patients/{self.patient.id}/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.patient.id)
        self.assertTrue(len(resp.data), 1)

    def test_update(self):
        patch_data = {
            "first_name": "SHOULD NOT BE CHANGED",
            "last_name": "SHOULD NOT BE CHANGED",
            # "phone_number": "+380965639682",
            "check_in_date": "SHOULD NOT BE CHANGED",

            "diagnosis": "Updated diagnosis, based on the new symptoms",
            "receipt": "Added some meds, that were not needed before"
        }

        resp = self.client.patch(f'/v1/patients/{self.patient.id}/', patch_data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['diagnosis'], patch_data['diagnosis'])
        self.assertEqual(resp.data['receipt'], patch_data['receipt'])

        self.patient.refresh_from_db()

        self.assertEqual(self.patient.diagnosis, patch_data['diagnosis'])
        self.assertEqual(self.patient.receipt, patch_data['receipt'])

        self.assertNotEquals(self.patient.first_name, patch_data['first_name'])
        self.assertNotEquals(self.patient.last_name, patch_data['last_name'])

    def test_phone_number(self):
        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['phone_number'], self.patient_data['phone_number'])