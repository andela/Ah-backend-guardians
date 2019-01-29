
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import ProfileSerializer, ReadingStatsSerializer
from .models import Profile, ReadingStat
from .exceptions import (ProfileDoesNotExist, UserCannotEditProfile,
                         exception_messages)
from .renderers import ProfileJSONRenderer, ReadingStatsJSONRenderer
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
            return Profile.objects.get(user=self.request.user,
                                       user__username=username)
        except Profile.DoesNotExist:
            raise PermissionDenied({
                'error':  exception_messages.get('edit_profile_no\
t_permitted').format(username)
            })


class ListProfileView(generics.ListAPIView):
    """
    Implements get all user profile endpoint
    """
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class FollowProfileView(generics.UpdateAPIView):
    """View class to handle user's follower operations
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """Method to follow a user's profile
        """
        username = request.data.get('username', {})

        if request.user.username == username:
            response_data = {
                'message': 'Sorry, you cannot follow yourself!'}

            return Response(data=response_data,
                            status=status.HTTP_400_BAD_REQUEST)

        toggler_response = Profile.objects.toggle_follow(
            request.user, username)
        if toggler_response is None or toggler_response == []:
            response_data = {
                'message': 'Please enter a valid username!'}

            return Response(data=response_data,
                            status=status.HTTP_400_BAD_REQUEST)
        if not toggler_response[1]:
            response_data = {
                'message': 'You have unfollowed {}!'.format(username)}

            return Response(data=response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'message': 'You have followed {}!'.format(username)}
            return Response(data=response_data, status=status.HTTP_200_OK)


class RetrieveFollowersView(generics.ListAPIView):
    """View class for retrieving all followers
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Method to get and return all a user's followers
        """
        user = request.user

        user_id = User.objects.filter(email=user.email).values('id')[
            0]['id']
        queryset = Profile.objects.get(user__pk=user_id).followers.all()

        followers = []
        for follower in queryset:
            follower_name = User.objects.get(email=follower.email)
            follower_username = follower_name.username
            followers.append(follower_username)
        if followers is None or followers == []:
            msg = {'message': 'No followers were found!'}
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        msg = {'followers': followers}
        return Response(data=msg, status=status.HTTP_200_OK)


class RetrieveFollowingView(generics.ListAPIView):
    """View class for retrieving all followers
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Method to get and return all a user's followers
        """
        user = request.user

        user_id = User.objects.filter(email=user.email).values('id')[
            0]['id']
        queryset = User.objects.filter(pk=user_id).first().is_following.all()

        following = []
        for follower in queryset:
            following_name = User.objects.get(username=follower)
            following_username = following_name.username
            following.append(following_username)
        if following is None or following == []:
            msg = {'message': 'You are not following anyone yet!'}
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        msg = {'following': following}
        return Response(data=msg, status=status.HTTP_200_OK)


class ReadingStatsView(generics.ListAPIView):
    """View class for retrieving the reading statistics of a user"""
    permission_classes = (IsAuthenticated, )
    serializer_class = ReadingStatsSerializer
    renderer_classes = (ReadingStatsJSONRenderer, )

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs.get('username')
        records = ReadingStat.objects.all().filter(user=user)

        return [articles.articles for articles in records]

    def get(self, request, username):

        if username != request.user.username:
            raise PermissionDenied({
                "message": "Unauthorized to view these stats"
            })
        articles = self.get_queryset()
        total_read_time = 0
        for article in articles:
            total_read_time += article.read_time

        data = {
            'user': request.user.username,
            'no._of_articles_read': len(articles),
            'total_read_time': total_read_time,
            'recent_articles': [article.id for article in articles[:5]],
        }
        return Response(data)
