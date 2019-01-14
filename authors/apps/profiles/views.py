
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import ProfileSerializer
from .models import Profile
from .exceptions import ProfileDoesNotExist, UserCannotEditProfile, exception_messages
from .renderers import ProfileJSONRenderer
from authors.apps.authentication.models import User

class RetrieveProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            username = self.kwargs.get("username")
            return get_object_or_404(Profile, user__username=username)
        except:
            raise ProfileDoesNotExist


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        try:
            # Profile.objects.get(user=self.request.user, user__username=username)
            return Profile.objects.get(user=self.request.user, user__username=username)
            # return get_object_or_404(Profile, user=self.request.user, user__username=username)
        except Profile.DoesNotExist:
            raise PermissionDenied({
                'error':  exception_messages.get('edit_profile_not_permitted').format(username)
            })


class ListProfileView(generics.ListAPIView):
    """
    Implements get all user profile endpoint
    """
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
