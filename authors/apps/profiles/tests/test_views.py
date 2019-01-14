import json

from django.urls import reverse

from rest_framework.views import status

from .base import BaseTestCase

from ..models import Profile

from authors.apps.profiles.tests.data import user2, user1

from authors.apps.authentication.models import User


# from .data import user_update, user1, user2, login_info


class RetrieveProfileTestCase(BaseTestCase):
    def setUp(self):
        username = user2['username']
        self.user = User.objects.get(username=username)

        self.url = reverse("profiles:profile_details", args=[username])

    def test_get_profile(self):
        """
        Test whether a user can get a profile
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data['email'], user2['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthroized_user_cannot_get_profile(self):
        """
        Test whether an unauthorized user can view a profile
        """
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EditProfileTestCase(BaseTestCase):
    def setUp(self):

        username1 = user1['username']
        username2 = user2['username']
        self.user = User.objects.get(username=username2)
        self.url1 = reverse("profiles:update_profile", args=[username1])
        self.url2 = reverse("profiles:update_profile", args=[username2])

    def test_unauthorized_to_edit_profile(self):
        """
        Editing a profile that does not belong to you
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url1)
        print(response.data)
        self.assertEqual(response.data['error'],
                         "You are not authorised to edit soultek's profile")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
