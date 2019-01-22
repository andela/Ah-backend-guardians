from rest_framework.test import APITestCase
from .data import wrong_fb_token, fb_token, google_token, twitter_token
from rest_framework.views import status
from django.urls import reverse
from unittest.mock import patch


class TestSocialLogin(APITestCase):

    def setUp(self):
        self.fb_url = reverse("authentication:fb_login")
        self.google_url = reverse("authentication:google_login")
        self.twitter_url = reverse("authentication:twitter_login")

    @patch('facebook.GraphAPI.get_object')
    def test_fb_login_new(self, get_object):
        get_object.return_value = dict(
            email="someemail@example.com",
            name="Author's Haven"
        )
        response = self.client.post(self.fb_url, fb_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('facebook.GraphAPI.get_object')
    def test_fb_login_return_user(self, get_object):
        get_object.return_value = dict(
            email="someemail@example.com",
            name="Author's Haven"
        )
        self.client.post(self.fb_url, fb_token, format="json")
        response = self.client.post(self.fb_url, fb_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('facebook.GraphAPI', side_effect=Exception())
    def test_fb_login_wrong_token(self, GraphAPI):
        response = self.client.post(self.fb_url, wrong_fb_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login_new_user(self, verify_oauth2_token):
        verify_oauth2_token.return_value = dict(
            email="someemail@example.com",
            name="Author's Haven"
        )
        response = self.client.post(
            self.google_url, google_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login_return_user(self, verify_oauth2_token):
        verify_oauth2_token.return_value = dict(
            email="someemail@example.com",
            name="Author's Haven"
        )
        self.client.post(self.google_url, google_token, format="json")
        response = self.client.post(
            self.google_url, google_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('google.oauth2.id_token.verify_oauth2_token', side_effect=Exception())
    def test_test_google_login_wrong_token(self, verify_oauth2_token):

        response = self.client.post(
            self.google_url, google_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_new_user(self, VerifyCredentials):
        VerifyCredentials.return_value.__dict__ = dict(
            email="someemail@example.com",
            name="Author's Haven"
        )
        response = self.client.post(
            self.twitter_url, twitter_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_return_user(self, VerifyCredentials):
        VerifyCredentials.return_value.__dict__ = dict(
            email="someemail@example.com",
            name="Author's Haven"
        )
        self.client.post(self.twitter_url, twitter_token, format="json")
        response = self.client.post(
            self.twitter_url, twitter_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('twitter.Api.VerifyCredentials', side_effect=Exception())
    def test_twitter_login_wrong_token(self, VerifyCredentials):
        response = self.client.post(self.twitter_url, fb_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
