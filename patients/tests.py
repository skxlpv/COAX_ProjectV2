from mixer.backend.django import mixer
from phonenumber_field.phonenumber import PhoneNumber

from api.tests import BaseAPITest
from hospitals.models import Department, City, Hospital
from patients.models import Patient


class TestPatientViewSet(BaseAPITest):
    def setUp(self):
        self.department = mixer.blend(Department)
        self.city = mixer.blend(City)
        self.hospital = mixer.blend(Hospital)
        self.hospital.hospital_departments.set([self.department.pk])

        self.user = self.create_and_login(hospital=self.hospital)

        self.patient = mixer.blend(Patient, doctor=self.user)

    def test_create(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLastName",
            "phone_number": "+380960000000"
        }

        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data['first_name'], self.patient_data['first_name'])

    def test_create_no_phone(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLastName",
            "phone_number": ""
        }

        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data['phone_number'], self.patient_data['phone_number'])

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

    def test_update_no_data(self):
        self.invalid_patch_data = {
            # NO DIAGNOSIS AND RECEIPT, NO DATA AT ALL
        }

        # the DIAGNOSIS and RECEIPT data stays the same after no data was passed
        resp = self.client.patch(f'/v1/patients/{self.patient.id}/', data=self.invalid_patch_data)
        self.assertEqual(resp.status_code, 200)

        self.patient.refresh_from_db()

        self.assertEqual(self.patient.diagnosis, self.patient.diagnosis)
        self.assertEqual(self.patient.receipt, self.patient.receipt)

        self.assertNotEquals(self.patient.diagnosis, self.invalid_patch_data)
        self.assertNotEquals(self.patient.receipt, self.invalid_patch_data)

    def test_phone_number(self):
        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['phone_number'], self.patient_data['phone_number'])
