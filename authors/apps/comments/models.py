from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class Comment(models.Model):

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE)
    parent = models.IntegerField(blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author)


class LikeComment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
