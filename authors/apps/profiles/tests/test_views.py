import json

from django.urls import reverse

from rest_framework.views import status

from .base import BaseTestCase

from ..models import Profile

from authors.apps.profiles.tests.data import user2, user1, follow_user,\
 follow_self, follow_non_existent_user

from authors.apps.authentication.models import User


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
        self.assertEqual(response.data['error'],
                         "You are not authorised to edit soultek's profile")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ListProfileTestCase(BaseTestCase):
    def setUp(self):
        username1 = user1['username']
        username2 = user2['username']
        self.user = User.objects.get(username=username2)

    def test_get_all_user_profiles(self):
        """
        Test whether a user can get all profiles
        """
        url = reverse("profiles:show_profile")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FollowProfileTestCase(BaseTestCase):
    """Class to test user follow features
    """

    def setUp(self):
        self.user = User.objects.get(username=user1['username'])
        self.url = reverse('profiles:follow_user')
        self.url2 = reverse('profiles:followers')
        self.url3 = reverse('profiles:following')
        self.user2 = User.objects.get(username=user2['username'])

    def test_follow_user(self):
        """Method to test whether a user's profile can be followed
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=follow_user, format='json')
        self.assertEqual(response.data['message'],
                         'You have followed bgpeter!')

    def test_user_cannot_follow_themselves(self):
        """Method to test that a user cannot follow themselves
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=follow_self, format='json')
        self.assertEqual(response.data['message'],
                         'Sorry, you cannot follow yourself!')

    def test_view_followers(self):
        """Method to test that a user can view all their followers
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=follow_user, format='json')
        self.assertEqual(response.data['message'],
                         'You have followed bgpeter!')
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url2)
        self.assertEqual(response.data['followers'], ['soultek'])

    def test_view_following(self):
        """Method to test that a user can view all the users they're following
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=follow_user, format='json')
        self.assertEqual(response.data['message'],
                         'You have followed bgpeter!')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url3)
        self.assertEqual(response.data['following'], ['bgpeter'])

    def test_cannot_follow_non_existent_profile(self):
        """Method to test that a user cannot follow a user who does not exist
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=follow_non_existent_user,
                                   format='json')
        self.assertEqual(response.data['message'],
                         'Please enter a valid username!')

    def test_retrieve_followers_without_followers(self):
        """Method to test that a user cannot retrieve that don't exist
        """
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url2)
        self.assertEqual(response.data['message'], 'No followers were found!')
