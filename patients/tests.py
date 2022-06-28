import datetime

from mixer.backend.django import mixer

from api.tests import BaseAPITest
from hospitals.models import Department, City, Hospital
from patients.models import Patient


class TestPatientViewSet(BaseAPITest):
    def setUp(self):
        self.department = mixer.blend(Department)
        self.city = mixer.blend(City)
        self.hospital1 = mixer.blend(Hospital)
        self.hospital2 = mixer.blend(Hospital)
        self.hospital1.hospital_departments.set([self.department.pk])
        self.hospital2.hospital_departments.set([self.department.pk])

        self.patient1 = mixer.blend(Patient, phone_number='+3809600000000')
        self.patient2 = mixer.blend(Patient, phone_number='+3809600000001')

        self.user = self.create_and_login()

    def test_create(self):
        self.user = self.create_and_login(hospital=self.hospital1, email='test3@test3.com')

        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLastName",
            "phone_number": "+380960000000",
            "doctor": self.user.id
        }

        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)

        patient = Patient.objects.filter(first_name='Test', last_name='TestLastName')

        self.assertTrue(patient.exists())

    def test_create_no_phone(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLastName",
            "doctor": self.user.id,
        }

        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['phone_number'], '')

    def test_list(self):
        resp = self.client.get('/v1/patients/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'], Patient.objects.all().count())

    def test_detail(self):
        resp = self.client.get(f'/v1/patients/{self.patient1.id}/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.patient1.id)
        self.assertTrue(len(resp.data), 1)

    def test_update(self):
        patch_data = {
            "diagnosis": "Updated diagnosis, based on the new symptoms",
            "receipt": "Added some meds, that were not needed before"
        }

        resp = self.client.patch(f'/v1/patients/{self.patient1.id}/', patch_data)
        self.assertEqual(resp.status_code, 200)

        self.patient1.refresh_from_db()

        self.assertEqual(resp.data['diagnosis'], patch_data['diagnosis'])
        self.assertEqual(resp.data['receipt'], patch_data['receipt'])

        self.assertEqual(self.patient1.diagnosis, patch_data['diagnosis'])
        self.assertEqual(self.patient1.receipt, patch_data['receipt'])

    def test_update_no_data(self):
        # start initializing default data
        self.valid_patch_data = {
            "diagnosis": "DIAGNOSIS",
            "receipt": "RECEIPT"
        }

        resp = self.client.patch(f'/v1/patients/{self.patient1.id}/', data=self.valid_patch_data)
        # end initializing default data

        self.invalid_patch_data = {
            # NO DIAGNOSIS AND RECEIPT, NO DATA AT ALL
        }

        # the DIAGNOSIS and RECEIPT data stays the same after no data was passed
        resp = self.client.patch(f'/v1/patients/{self.patient1.id}/', data=self.invalid_patch_data)

        self.assertEqual(resp.status_code, 200)

        self.patient1.refresh_from_db()

        self.assertEqual(self.patient1.diagnosis, 'DIAGNOSIS')
        self.assertEqual(self.patient1.receipt, 'RECEIPT')

    def test_phone_number(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLastName",
            "doctor": self.user.id,
            "phone_number": "+380960000000"
        }

        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['phone_number'], self.patient_data['phone_number'])

    def test_created_at(self):
        self.patient_data = {
            "first_name": "Test",
            "last_name": "TestLastName",
            "doctor": self.user.id,
            "phone_number": "",
            "created_at": datetime.date(2020,2,24)
        }

        resp = self.client.post('/v1/patients/', self.patient_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['created_at'], f"{self.patient_data['created_at']}")
