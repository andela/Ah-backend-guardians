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
    start_index = models.IntegerField(blank=True, null=True)
    end_index = models.IntegerField(blank=True, null=True)
    selected_text = models.TextField(blank=True, null=True)


class LikeComment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class EditHistory(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.body)
