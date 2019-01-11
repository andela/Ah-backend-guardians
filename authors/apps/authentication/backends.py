import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """Authenticate the user """
        request.user = None
        # get a list of the items in the header
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if len(auth_header) == 2:
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')
            if prefix.lower() != auth_header_prefix:
                msg = 'Token is expected as the prefix '
                raise exceptions.AuthenticationFailed(msg)
            else:
                return self._authenticate_credentiatials(request, token)
        else:
            msg = 'The header must contain only two elements'
            raise exceptions.AuthenticationFailed(msg)

    def _authenticate_credentiatials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(pk=payload['id'])
            if not user.is_active:
                msg = 'This user has been deactivated'
                raise exceptions.AuthenticationFailed(msg)
            return (user, token)
        except:
            msg = 'Invalid authentication. Could not decode token'

            raise exceptions.AuthenticationFailed(msg)
