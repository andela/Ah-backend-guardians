from rest_framework.permissions import IsAuthenticated
from .models import Notification
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .serializers import NotificationSerializer


class ListNotificationsView(ListAPIView):
    """View class to handle fetching all notifications and updating their status.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """Method to fetch all notifications
        """
        user = self.request.user

        notifications = user.profile.notification_receiver.all()

        return notifications
