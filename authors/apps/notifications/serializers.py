from rest_framework import serializers

from authors.apps.authentication.serializers import UserSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'sender', 'receiver', 'read_status', 'message',
                  'action_link', 'email_status', 'created_at')
        model = Notification
