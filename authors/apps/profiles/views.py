
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import ProfileSerializer, EditProfileSerializer
from .models import Profile
from .exceptions import exception_messages, exception_message2
from .renderers import ProfileJSONRenderer
from authors.apps.authentication.models import User


class RetrieveProfileView(generics.RetrieveAPIView):
    """
    Implements get a user endpoint
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Function that returns an existing profile
        and the corresponding error message if the profile
        does not exist
        """
        try:
            username = self.kwargs.get("username")
            return Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise PermissionDenied({
                'error':  exception_message2.get('edit_profile_does_not_exist')
            })


class UpdateProfileView(generics.UpdateAPIView):
    """
    Implements edit a user endpoint
    """
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = EditProfileSerializer

    def get_object(self):
        """
        Fuvtion that enables a user to edit a profile if he
        has the correct credentials and the corresponding
        error message if a user does not have the necessary
        """
        username = self.kwargs.get("username")
        try:
            return Profile.objects.get(user=self.request.user,
                                       user__username=username)
        except Profile.DoesNotExist:
            raise PermissionDenied({
                'error':  exception_messages.get
                ('edit_profile_not_permitted').format(username)
            })
