from mixer.backend.django import mixer

from api.tests import BaseAPITest
from hospitals.models import Department, City, Hospital
from patients.models import Patient


class TestPatientViewSet(BaseAPITest):
    def setUp(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLast",
            "diagnosis": "Some Diagnosis",
            "receipt": "Some Receipt"
        }
        self.department = mixer.blend(Department)
        self.city = mixer.blend(City)
        self.hospital = mixer.blend(Hospital)
        self.hospital.hospital_departments.set([self.department.pk])

        self.user = self.create_and_login(hospital=self.hospital)

        self.patient1 = mixer.blend(Patient, doctor=self.user)
        self.patient2 = mixer.blend(Patient, doctor=self.user)
        self.patient3 = mixer.blend(Patient, doctor=self.user)

    def test_create(self):
        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertFalse(isinstance(resp.data, Patient))
        self.assertTrue(resp.data['first_name'], self.patient_data['first_name'])

    def test_list(self):
        resp = self.client.get('/v1/patients/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data['results']), Patient.objects.all().count())

    def test_detail(self):
        resp = self.client.get(f'/v1/patients/{self.patient1.id}/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.patient1.id)
        self.assertTrue(len(resp.data), 1)

    def test_update(self):
        patch_data = {
            "first_name": "SHOULD NOT BE CHANGED",
            "last_name": "SHOULD NOT BE CHANGED",
            "phone_number": "SHOULD NOT BE CHANGED",
            "check_in_date": "SHOULD NOT BE CHANGED",

            "diagnosis": "Updated diagnosis, based on the new symptoms",
            "receipt": "Added some meds, that were not needed before"
        }

        resp = self.client.patch(f'/v1/patients/{self.patient1.id}/', patch_data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['diagnosis'], patch_data['diagnosis'])
        self.assertEqual(resp.data['receipt'], patch_data['receipt'])

        self.patient1.refresh_from_db()

        self.assertEqual(self.patient1.diagnosis, patch_data['diagnosis'])
        self.assertEqual(self.patient1.receipt, patch_data['receipt'])

        self.assertNotEquals(self.patient1.first_name, patch_data['first_name'])
        self.assertNotEquals(self.patient1.last_name, patch_data['last_name'])
