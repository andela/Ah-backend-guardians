from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class ProfileManager(models.Manager):
    """Class to handle follower toggles
    """

    def toggle_follow(self, request_user, username):
        """Method to follow a user incase they're not following them and
        unfollow in case they're following
        """
        try:
            user_id = User.objects.filter(username=username).values('id')[
                0]['id']

            profile = Profile.objects.get(user_id=user_id)
            is_following = False

            if request_user in profile.followers.all():
                profile.followers.remove(request_user)
            else:
                profile.followers.add(request_user)
                is_following = True
            return profile, is_following
        except IndexError:
            return None


class Profile(models.Model):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='is_following',
                                       blank=True, symmetrical=False)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()


class ReadingStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             to_field='username')
    articles = models.ForeignKey(Article, on_delete=models.CASCADE,
                                 to_field='slug')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
