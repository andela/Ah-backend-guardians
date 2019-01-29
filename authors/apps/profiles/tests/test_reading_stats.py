from django.urls import reverse

from rest_framework.views import status

from .base import BaseTestCase
from .data import user1, user2
from authors.apps.authentication.models import User


class ReadingStatsTest(BaseTestCase):

    def setUp(self):
        username = user1['username']
        self.user1 = User.objects.get(username=username)
        self.url = reverse('profiles:reading_stats', args=[username])

        username2 = user2['username']
        self.user2 = User.objects.get(username=username2)
        self.url2 = reverse('profiles:reading_stats', args=[username2])

    def test_get_reading_stats_with_reads(self):
        """Tests that users' reading stats are returned"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reading_stats_for_another_user(self):
        """Tests that users aren't authorised to view others' reading stats"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.data['message'],
                         'Unauthorized to view these stats')
