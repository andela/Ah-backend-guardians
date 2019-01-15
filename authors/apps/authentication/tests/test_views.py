import json
from django.urls import reverse

from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient

from .base import BaseTestCase

from ..models import User

from .data import user_update, user1, user2, user3, verify_user1, login_info, \
    incorrect_email, userp, email, password, no_email, \
    logged_in_user2, bad_login_info1, bad_login_info2, inactive_account, \
    inactive_login_info, decode_error, prefix_error


class RegistrationLoginViewTestCase(BaseTestCase):

    def test_verification_sent(self):
        response = self.register_user(user1)
        self.assertEqual(response.data['msg'], verify_user1['msg'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_activated(self):
        register = self.register_user(user1)
        response = self.client.get(register.data['route'], format='json')
        self.assertEqual(response.data['msg'],
                         'Your account has been activated, congratulations')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activation_link_invalid(self):
        url = '/api/users/530-9fea92310fa49fe3/c3Nkc3Nlc3NkczIzZDQ0c3Nmc2U/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['error']['detail'],
                         'Activation link is invalid!')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_account_not_active(self):
        """Test api cannot login user if account is not activated"""
        response = self.log_in_user(inactive_login_info)
        self.assertEqual(response.data['errors']['error'],
                         [inactive_account['error']])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_credentials(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(login_info)
        self.assertEqual(response.data['username'],
                         logged_in_user2['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_null_email(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(bad_login_info1)

        self.assertEqual(response.data['errors']['email'], [
                         'This field may not be null.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_email(self):
        """Test api can login user if user password and email match"""
        response = self.log_in_user(bad_login_info2)

        self.assertEqual(response.data['errors']['email'], [
                         'This field may not be blank.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateViewTestCase(BaseTestCase):

    def setUp(self):
        login_response = self.log_in_user(login_info)
        self.token = login_response.data['token']
        self.url = reverse("authentication:detail")

    def test_get_user_credentials_when_authenticated(self):
        """Test api can get user if user is authenticated"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.data['username'], user3['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_decode_error(self):
        """Test api can't returns decode error"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer 89765423242524afgdbhdhh')
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'], decode_error)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_Bearer_expected_error(self):
        """Test api can get user if user is authenticated"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token 89765423242524afgdbhdhh')
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'], prefix_error)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_user_credentials_when_authenticated(self):
        """Test api can edit user data if user is authenticated"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
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
