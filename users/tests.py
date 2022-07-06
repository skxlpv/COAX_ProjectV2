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

        self.old_password = {
            "old_password": "test_password"
        }

        self.password = {
            "old_password": self.old_password["old_password"],
            "password": "dafFArgv34gFFgv"
        }

        self.data = {
            "first_name": "changed",
            "email": "test2@gmail.com"
        }

    def test_change_password(self):
        resp = self.client.patch(reverse('v1:users:profile-change-password'),
                                 data=self.password)
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password['password']))

    def test_change_password_validation_error(self):
        resp = self.client.patch(reverse('v1:users:profile-change-password'),
                                 data={"old_password": self.old_password["old_password"],
                                       "password": "a"})
        self.assertEqual(resp.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password["old_password"]))

    def test_change_password_old_wrong(self):
        resp = self.client.patch(reverse('v1:users:profile-change-password'),
                                 data={"old_password": "wrong_old",
                                       "password": "test_password12167"})
        self.assertEqual(resp.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password["old_password"]))

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

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, self.user2.email)

    def test_change_email_validation_error(self):
        resp = self.client.patch(reverse('v1:users:profile-edit'),
                                 data={"email": "a@a.a"})

        self.assertEqual(resp.status_code, 400)

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, resp.data.serializer.data["email"])

    def test_my_profile(self):
        resp = self.client.get('/v1/users/my-profile/') # this is simple path() URL

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['email'], self.user.email)
