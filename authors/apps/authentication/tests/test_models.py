from django.test import TestCase

from ..models import User, UserManager

from .data import (
    user_data, user_data_no_username, user_data_no_email,
    super_user_data, super_user_data_no_password,
    super_user_data_no_username
    )


class UserModelTestCase(TestCase):

    def setUp(self):
        """ Creates an instance of the User """
        self.user1 = User.objects.create_user(**user_data)

    def test_create_user(self):
        """test that user is created"""
        self.assertIsInstance(self.user1, User)

    def test_user_respresentations(self):
        """test that user object string representation is returned"""
        self.assertTrue(self.user1.email, str(self.user1))

    def test_get_short_name(self):
        """test that user can get short name"""
        self.assertTrue(self.user1.get_short_name(), user_data['username'])

    def test_get_full_name(self):
        """test that user can get full name"""
        self.assertTrue(self.user1.get_full_name, user_data['username'])

    def test_create_user_if_no_email(self):
        """test that user is not created because no email"""
        error_msg = 'Users must have an email address.'
        with self.assertRaisesMessage(TypeError, error_msg):
            User.objects.create_user(**user_data_no_email)

    def test_create_user_if_no_username(self):
        """test that user is not created because no username"""
        error_msg = 'Users must have a username.'
        with self.assertRaisesMessage(TypeError, error_msg):
            User.objects.create_user(**user_data_no_username)

    def test_create_super_user_is_staff(self):
        """test that super user is created"""
        user = User.objects.create_superuser(**super_user_data)
        self.assertTrue(user.is_staff)

    def test_create_super_user(self):
        """test that super user is created"""
        user = User.objects.create_superuser(**super_user_data)
        self.assertIsInstance(user, User)

    def test_create_super_user_is_super_user(self):
        """test that super user is created"""
        user = User.objects.create_superuser(**super_user_data)
        self.assertTrue(user.is_superuser)

    def test_create_super_user_if_no_username(self):
        """test that user is not created because no username"""
        error_msg = 'Users must have a username.'
        with self.assertRaisesMessage(TypeError, error_msg):
            User.objects.create_superuser(**super_user_data_no_username)

    def test_create_super_user_if_no_password(self):
        """test that user is not created because no username"""
        error_msg = 'Superusers must have a password.'
        with self.assertRaisesMessage(TypeError, error_msg):
            User.objects.create_superuser(**super_user_data_no_password)
