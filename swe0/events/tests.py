from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
import pytz

from swe0.events.models import CheckIn, Event


User = get_user_model()


class CheckInTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            name='User',
            email='test@example.com',
            password='password',
        )
        cls.event = Event.objects.create(
            title='Test Event',
            start_time=datetime(2020, 2, 2, tzinfo=pytz.utc),
            check_in_enabled=True,
            check_in_code='test',
        )

    def test_success(self):
        self.client.login(email='test@example.com', password='password')
        self.client.post('/events/check-in/', {'check_in_code': 'test'})
        self.assertQuerysetEqual(
            CheckIn.objects.all(),
            ['<CheckIn: User <test@example.com> at Test Event>'],
        )

    def test_duplicate(self):
        self.client.login(email='test@example.com', password='password')
        self.client.post('/events/check-in/', {'check_in_code': 'test'})
        self.client.post('/events/check-in/', {'check_in_code': 'test'})
        self.assertEqual(CheckIn.objects.count(), 1)

    def test_incorrect(self):
        self.client.login(email='test@example.com', password='password')
        self.client.post('/events/check-in/', {'check_in_code': 'incorrect'})
        self.assertEqual(CheckIn.objects.count(), 0)

    def test_disabled(self):
        self.client.login(email='test@example.com', password='password')
        Event.objects.create(
            start_time=datetime(2020, 2, 2, tzinfo=pytz.utc),
            check_in_enabled=False,
            check_in_code='disabled'
        )
        self.client.post('/events/check-in/', {'check_in_code': 'disabled'})
        self.assertEqual(CheckIn.objects.count(), 0)

    def test_unauthenticated(self):
        self.client.post('/events/check-in/', {'check_in_code': 'test'})
        self.assertEqual(CheckIn.objects.count(), 0)
