from authors.apps.profiles.models import Profile
from django.db import models
from django.contrib.auth.models import BaseUserManager


class NotificationsManager(models.Manager):
    """Manager model for notifications operations
    """

    def add_notification(self, sender, receiver, message, action_link):
        """Method to create a notification
        """
        notification = self.model(sender=sender, receiver=receiver,
                                  message=message, action_link=action_link)
        notification.save()

        return notification


class Notification(models.Model):
    """Model to handle notifications
    """
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='notification_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                 related_name='notification_receiver')
    read_status = models.BooleanField(default=False)
    message = models.CharField(max_length=255)
    action_link = models.CharField(max_length=255, null=True)
    email_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = NotificationsManager()

    def __str__(self):
        """Method to return the message from the notification
        """
        return self.message
