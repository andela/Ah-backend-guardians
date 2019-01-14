from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.apps.authentication.models import User

class Profile(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/avatar/',blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()


