from django.urls import reverse
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):

    fixtures = ['authors/apps/authentication/tests/fixtures/user.json',
                'authors/apps/articles/tests/fixtures/user.json',
                'authors/apps/articles/tests/fixtures/articles.json']

    def register_user(self, signup_data):
        url = reverse("authentication:register")
        response = self.client.post(url, signup_data, format="json")

        return response

    def log_in_user(self, login_data):

        url = reverse("authentication:login")
        response = self.client.post(url, login_data, format="json")

        return response
