from django.urls import reverse

from rest_framework.views import status

from .base import BaseTestCase

from ..models import User

from .data import user_update, user1, user2, login_info


class RegistrationLoginViewTestCase(BaseTestCase):

    def test_register_new_user_correct_details(self):
        """Test api  can create user"""
        response = self.register_user(user1)
        self.assertEqual(response.data['email'], user1['user']['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_valid_credentials(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(login_info)

        self.assertEqual(response.data['username'], user2['user']['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRetrieveUpdateViewTestCase(BaseTestCase):
    def setUp(self):
        self.user = User.objects.get(username=user2['user']['username'])
        self.client.force_authenticate(user=self.user)
        self.url = reverse("authentication:detail")

    def test_get_user_credentials_when_authenticated(self):
        """Test api can get user if user is authenticated"""
        response = self.client.get(self.url)
        self.assertEqual(response.data['username'], user2['user']['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_user_credentials(self):
        """Test api can edit user data if user is authenticated"""
        # update user data
        response = self.client.put(self.url, user_update, format="json")
        username = user_update['user']['username']
        self.assertEqual(response.data['username'], username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
