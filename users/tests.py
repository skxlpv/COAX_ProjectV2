from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.tests import BaseAPITest
from hospitals.models import Hospital


class TestUserApiView(BaseAPITest):
    def setUp(self):
        self.hospital = mixer.blend(Hospital)
        self.create_and_login(hospital=self.hospital, is_writer=True)

    def test_change_password(self):
        resp = self.client.patch(reverse('v1:users:profile-change-password'))
        self.fail('no test')

    def test_change_password_validation_error(self):
        self.fail('no test')

    def test_change_data(self):
        self.fail('no test')

    def test_change_email_exist(self):
        self.fail('no test')

    def test_change_email_validation_error(self):
        self.fail('no test')
