from django.urls import reverse
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):

    fixtures = ['authors/apps/profiles/tests/fixtures/profile.json',
                'authors/apps/profiles/tests/fixtures/user.json',
                'authors/apps/profiles/tests/fixtures/stats.json']
