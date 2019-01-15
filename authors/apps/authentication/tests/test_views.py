import json
from django.urls import reverse

from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient

from .base import BaseTestCase

from ..models import User

from .data import user_update, user1, user2, login_info, \
     incorrect_email, userp, email, password, no_email, \
     bad_login_info1, bad_login_info2


class RegistrationLoginViewTestCase(BaseTestCase):

    def test_register_new_user_correct_details(self):
        """Test api  can create user"""
        response = self.register_user(user1)
        self.assertEqual(response.data['email'], user1['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_valid_credentials(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(login_info)

        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_null_email(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(bad_login_info1)
        print(response.data)

        self.assertEqual(response.data['errors']['email'], ['This field may not be null.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_email(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(bad_login_info2)
        print(response.data)

        self.assertEqual(response.data['errors']['email'], ['This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_successfully_token_returned(self):
        """Test a user gets back a JWT when they register succesfully"""
        response = self.register_user(user1)

        self.assertTrue(response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserRetrieveUpdateViewTestCase(BaseTestCase):
    def setUp(self):
        self.user = User.objects.get(username=user2['username'])
        self.client.force_authenticate(user=self.user)
        self.url = reverse("authentication:detail")

    def test_get_user_credentials_when_authenticated(self):
        """Test api can get user if user is authenticated"""
        response = self.client.get(self.url)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_user_credentials(self):
        """Test api can edit user data if user is authenticated"""
        self.register_user(user1)
        response = self.client.put(self.url, user_update, format="json")
        username = user_update['username']
        self.assertEqual(response.data['username'], username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestResetPassword(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def user_logged_in(self):
        user = self.client.post('/api/users/', userp, format='json')
        return user

    def test_incorrect_email(self):
        TestResetPassword.user_logged_in(self)
        res = self.client.post(
            '/api/password-reset/', incorrect_email, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(res.content),
            {
                'errors': {
                    'email': [
                        'No User Found That Matches Entered Email'
                    ]
                }
            }
        )

    def test_correct_entered_email(self):
        TestResetPassword.user_logged_in(self)
        res = self.client.post(
            '/api/password-reset/', email, format='json')
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(res.content),
            {
                "message": "An Email Has Been Sent To This Email Address"
            }
        )

    def test_no_email(self):
        TestResetPassword.user_logged_in(self)
        res = self.client.post(
            '/api/password-reset/', no_email, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(res.content),
            {
                'errors': {
                    'email': [
                        'This field may not be blank.'
                    ]
                }
            }
        )

    def test_no_reset_password(self):
        self.short_password = {
            "password": "",
            "confirm_password": ""
        }
        TestResetPassword.user_logged_in(self)
        res = self.client.put(
            '/api/password-reset-confirm/sqr6-57Kb6dc3333efvbn1de-bHVnam9zaC',
            self.short_password,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(res.content),
            {
                'errors': {
                    'password': [
                        'This field may not be blank.'
                    ],
                    'confirm_password': [
                        'This field may not be blank.'
                    ]
                }
            }
        )

    def test_passwords_donot_match(self):
        self.unmatched_password = {
            "password": "moseskamira",
            "confirm_password": "mosesk"
        }
        TestResetPassword.user_logged_in(self)
        res = self.client.put(
            '/api/password-reset-confirm/sqr6-57Kb6dc3333efvbn1de-bHVnam9zaC',
            self.unmatched_password,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(res.content),
            {
                'errors': {
                    'body': [
                        'Password Mismatch, Please Re-enter Password'
                    ]
                }
            }
        )

    def test_confirmation_password(self):
        TestResetPassword.user_logged_in(self)
        res = self.client.put(
            '/api/password-reset-confirm/sqr6-57Kb6dc3333efvbn1de-bHVnam9zaC',
            password,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(res.content),
            {
                'message': {
                    'detail': [
                        'Password Has Been Successfully Reset, Please Login '
                    ]
                }
            })
