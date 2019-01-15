import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User

"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):
    """Class to handle all custom authentication for the application"""

    def authenticate(self, request):
        """Method to define custom authentication for requests and return a token"""
        pass
