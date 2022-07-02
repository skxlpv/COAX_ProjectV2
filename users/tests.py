from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.tests import BaseAPITest
from hospitals.models import Hospital
from users.models import User


class TestUserApiView(BaseAPITest):
    def setUp(self):
        self.hospital = mixer.blend(Hospital)
        self.user = self.create_and_login(hospital=self.hospital, is_writer=True)

        self.data = {
            "first_name": "changed",
            "email": "test2@gmail.com"
        }

    def test_change_password(self):
        resp = self.client.patch(reverse('v1:users:profile-change-password'),
                                 data={"password": "dafFArgv34gFFgv"})
        self.assertEqual(resp.status_code, 200)
        self.logout()
        self.authorize(self.user)
        self.assertEqual(resp.status_code, 200)

    def test_change_password_validation_error(self):
        resp = self.client.patch(reverse('v1:users:profile-change-password'),
                                 data={"password": "a"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(*resp.data, 'non_field_errors')

    def test_change_data(self):
        resp = self.client.patch(reverse('v1:users:profile-edit'),
                                 data=self.data)
        self.assertEqual(resp.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, self.data["first_name"])
        self.assertEqual(self.user.last_name, 'test')

    def test_change_email_exist(self):
        self.user2 = self.create(email="exist@gmail.com")

        resp = self.client.patch(reverse('v1:users:profile-edit'),
                                 data={"email": "exist@gmail.com"})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['email'][0], 'user with this email already exists.')

    def test_change_email_validation_error(self):
        resp = self.client.patch(reverse('v1:users:profile-edit'),
                                 data={"email": "a@a.a"})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['email'][0], 'Enter a valid email address.')

    def test_my_profile(self):
        resp = self.client.get('/v1/users/my-profile/') # this is simple path() URL

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['email'], self.user.email)
