from django.urls import reverse
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):

    fixtures = ['authors/apps/comments/tests/fixtures/user.json',
                'authors/apps/comments/tests/fixtures/articles.json',
                'authors/apps/comments/tests/fixtures/comments.json',
                'authors/apps/comments/tests/fixtures/likes.json']

    def log_in_user(self, login_data):
        url = reverse("authentication:login")
        response = self.client.post(url, login_data, format="json")
        return response
