import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User

"""Configure JWT Here"""

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'token'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        
        if not auth_header:
            return None
        if len(auth_header) == 0:
            return None
        elif len(auth_header) > 2:
            return None
        
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        print(token)

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            raise exceptions.AuthenticationFailed('Cannot decode token!')
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user was found matching this token!')
        if not user.is_active():
            raise exceptions.AuthenticationFailed('This user was deactivated!')
        
        return (user, token)
