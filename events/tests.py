import datetime

from mixer.backend.django import mixer

from api.tests import BaseAPITest
from events.models import Event
from hospitals.models import Hospital


class TestEventViewSet(BaseAPITest):

    def setUp(self):
        self.hospital = mixer.blend(Hospital)

        self.user1 = self.create_and_login(email='someemail@email.com', hospital=self.hospital)
        self.user2 = self.create_and_login(email='someotheremail@email.com', hospital=self.hospital)

        self.event = mixer.blend(Event, creator=self.user1, hospital=self.hospital)

    def test_create(self):
        self.event_data = {
            'title': 'TESTTITLE',
            'type': 'OT'
        }

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data['title'], self.event_data['title'])

    def test_list(self):
        self.event1 = mixer.blend(Event, creator=self.user1, hospital=self.hospital)
        self.event2 = mixer.blend(Event, creator=self.user2, hospital=self.hospital)
        self.event3 = mixer.blend(Event, creator=self.user1, hospital=self.hospital)

        resp = self.client.get('/v1/events/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], Event.objects.all().count())

    def test_detail(self):
        resp = self.client.get(f'/v1/events/{self.event.id}/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], self.event.title)

    def test_delete(self):
        resp = self.client.delete(f'/v1/events/{self.event.id}/')

        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Event.objects.filter(title=self.event.title).exists())

    def test_start_time_correct_format(self):
        self.event_data = {
            'title': 'TESTTITLE',
            'type': 'OT',
            'start_time': datetime.date(2000, 1, 1)
        }

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['start_time'], '01/01/2000 00:00')

    def test_end_time_correct_format(self):
        self.event_data = {
            'title': 'TESTTITLE',
            'type': 'OT',
            'end_time': datetime.date(2000, 1, 1)
        }

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['end_time'], '01/01/2000 00:00')

    def test_create_no_time(self):
        self.event_data = {
            'title': 'TESTTITLE',
            'type': 'OT',
            'start_time': '',
            'end_time': ''
        }

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['start_time'], None)
        self.assertEqual(resp.data['end_time'], None)

    def test_blank_participants(self):
        self.event_data = {
            'title': 'TESTTITLE',
            'type': 'OT',
            'participants': []
        }

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['participants'], [])

    def test_default_event_type(self):
        self.default_value = 'OT'

        self.event_data = {
            'title': 'TESTTITLE',
            'type': ''
        }

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['type'], self.default_value)

    def test_create_error_no_required_fields(self):
        self.event_data = {}

        resp = self.client.post('/v1/events/', data=self.event_data)

        self.assertEqual(resp.status_code, 400)
