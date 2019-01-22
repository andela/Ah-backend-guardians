from rest_framework.views import status

from .base import BaseTestCase

from .data import *


class ValidationTest(BaseTestCase):
    def test_register_with_short_password(self):
        """Test api  can't create user if password is invalid"""

        response = self.register_user(short_password)

        self.assertEqual(response.data['errors']['password'], [
            "Ensure this field has at least 8 characters."])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_that_doesnot_follow_conventions(self):
        """Test api  can't create user if password is invalid"""

        response = self.register_user(poor_conventions_password)

        self.assertEqual(response.data['errors']['error'],
                         ["Ensure password has an uppercase, lowercase, "
                          "a numerical character and no leading or "
                          "trailing spaces."])

    def test_register_with_short_username(self):
        """Test api  can't create user if username is too short"""

        response = self.register_user(short_username)

        self.assertEqual(response.data['errors']['error'], [
            "Ensure username is atleast 4 characters long."])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_username(self):
        """Test api  can't create user if username has special characters"""

        response = self.register_user(invalid_username)

        self.assertEqual(response.data['errors']['error'], [
            "Ensure username has only letters, "
            "numbers or a combination of both."])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
