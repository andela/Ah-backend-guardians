from .models import Notification
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from authors import settings
from rest_framework import authentication
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from authors.apps.articles.models import Favourites


class NotificationAction:
    """Class to handle to operations of notifications
    """

    def profile_followed(self, request, follower, receiver):
        """Method to trigger a notification when a user is followed

        :params:

        follower - takes in the username of the follower.

        notification_receiver - takes in the username of the person who is
        being followed.
        """
        message = f'{follower} started following you!'
        action_link = request.build_absolute_uri(
            reverse(
                'profiles:profile_details', kwargs={
                    'username': follower.user.username
                })
        )
        self.trigger_in_app_notification(request, (follower, receiver, message,
                                                   action_link))
        if receiver.email_notification_permissions:
            current_site = get_current_site(request)
            domain = f'http://{current_site.domain}'
            route = reverse('profiles:profile_details',
                            kwargs={'username': follower.user.username}
                            )

            url = f'{domain}{route}'
            subject = "Author's Haven New Follower!"
            message = f'Click Link Below To View Their Profile\n{url}'
            self.trigger_email_notification(follower, request, subject,
                                            message)

    def trigger_in_app_notification(self, request, notification):
        """Method to trigger a notification either in-app or email or both
        based on the appropriate permissions given by the user
        """
        sender, receiver, message, action_link = notification
        notification = Notification.objects.add_notification(
            sender=sender,
            receiver=receiver,
            message=message,
            action_link=action_link
        )

    def trigger_email_notification(self, sender, request, subject, message):
        """Method to trigger email notification
        """
        user = request.user

        recipient_email = user.email
        application_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, application_email,
                  [recipient_email], fail_silently=False)

        return send_mail

    def article_created(self, request, followers, author, article_slug):
        """Method to notify users about an article from an author they follow
        """
        if followers != []:
            message = "Check out this new article\
 from {author}!\n\n".format(author=author)
            action_link = reverse('article:detail',
                                  kwargs={'slug': article_slug})
            for follower in followers:
                user_id = User.objects.filter(
                    username=follower.username
                ).values('id')[0]['id']
                follower_profile = Profile.objects.get(user_id=user_id)
                self.trigger_in_app_notification(request, (author,
                                                           follower_profile,
                                                           message,
                                                           action_link))
                if follower_profile.email_notification_permissions:

                    current_site = get_current_site(request)
                    domain = f'http://{current_site.domain}'
                    route = reverse('article:detail',
                                    kwargs={'slug': article_slug})

                    url = f'{domain}{route}'
                    subject = "Author's Haven New Article!"
                    message = f'Click Link Below To Read This Article\n{url}'
                    self.trigger_email_notification(follower, request, subject,
                                                    message)

    def comment_created(self, request, comment_author, article_author,
                        article_slug):
        """Method to notify a user when a comment is added to an article
        """
        message = f'{comment_author} commented on this article!'
        action_link = reverse('article:detail',
                              kwargs={'slug': article_slug})
        self.trigger_in_app_notification(request, (comment_author,
                                                   article_author, message,
                                                   action_link))
        if article_author.email_notification_permissions:
            current_site = get_current_site(request)
            domain = f'http://{current_site.domain}'
            route = reverse('article:detail',
                            kwargs={'slug': article_slug})

            url = f'{domain}{route}'
            subject = "Author's Haven New Comment!"
            message = f'Click The Link To View This Article and Comment\n\n\
{url}'
            self.trigger_email_notification(comment_author, request, subject,
                                            message)
        article = Article.objects.get(slug=article_slug)
        article_id = article.pk
        queryset = Favourites.objects.filter(article_id=article_id,
                                             favourite=True)
        if queryset != []:
            for favourite in queryset:
                user_id = favourite.user.pk
                reader_profile = Profile.objects.get(user_id=user_id)
                self.trigger_in_app_notification(request, (comment_author,
                                                           reader_profile,
                                                           message,
                                                           action_link))
                if reader_profile.email_notification_permissions:
                    current_site = get_current_site(request)
                    domain = f'http://{current_site.domain}'
                    route = reverse('article:detail',
                                    kwargs={'slug': article_slug})

                    url = f'{domain}{route}'
                    subject = "Author's Haven New Comment on Your Favourite\
 Article!"
                    message = f'Click The Link To View This Article and Comment\n\n\
{url}'
                    self.trigger_email_notification(comment_author, request,
                                                    subject, message)
