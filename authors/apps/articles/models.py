from django.db import models
from datetime import datetime, timedelta
from ..authentication.models import User
from django.db.models import Avg
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

from django.conf import settings


class Article(models.Model):
    """
    Class Implementing The Article Model.
    """

    title = models.CharField(db_index=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField(db_index=True)
    description = models.CharField(db_index=True, max_length=255)
    slug = models.SlugField(
        db_index=True, max_length=255, unique=True, blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = models.CharField(max_length=255, blank=True)
    read_time = models.PositiveSmallIntegerField(null=True)
    tags = ArrayField(models.CharField(max_length=255, unique=False,
                                       blank=True), unique=False, blank=True,
                      default=list)
    favourited = models.BooleanField(blank=True, default=False)
    favouriteCount = models.IntegerField(blank=True, default=0)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def average_rating(self):
        """
        This function calculates the average rating of the reviewed article
        """
        ratings = self.article_ratings.all().aggregate(score=Avg("score"))
        return float('%.2f' % (ratings["score"] if ratings['score'] else 0))

    def get_likes(self, **kwargs):
        """
        This method counts article likes
        params: dictionary
        return:number of likes
        """
        likes = kwargs.get('model').objects.all().filter(
            article_like=kwargs.get('like_article')
        )
        filtered_likes = likes.filter(article_id=kwargs.get('article_id'))
        return filtered_likes.count()

    def get_dislikes(self, **kwargs):
        """
        This method counts article dislikes
        params: dictionary
        return:number of dislikes
        """
        dislikes = kwargs.get('model').objects.all().filter(
            article_dislike=kwargs.get('dislike_article')
        )
        filtered_dislikes = dislikes.filter(
            article_id=kwargs.get('article_id'))
        return filtered_dislikes.count()

    @property
    def likes_count(self):
        """return count of liked article"""
        return self.get_likes(
            model=ArticleLikes,
            like_article=True,
            article_id=self.pk)

    @property
    def dislikes_count(self):
        """return count of unliked article"""
        return self. get_dislikes(
            model=ArticleDisLikes,
            dislike_article=True,
            article_id=self.pk)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    @staticmethod
    def count_words(article_body):
        total_words = 0
        for word in article_body:
            total_words += len(word)/settings.WORD_LENGTH
        return total_words

    def calculate_reading_time(self):
        """
        Method that calculates the reading time of an article
        """
        total_words = Article.count_words(self.body)
        return int(total_words/settings.WPM)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        if not self.read_time:
            self.read_time = self.calculate_reading_time()
        super(Article, self).save(*args, **kwargs)


class Rating(models.Model):
    """
    Model for rating an article
    """
    article = models.ForeignKey(
        Article, related_name='article_ratings',
        on_delete=models.CASCADE, null=True)
    reader = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="article_ratings", null=True)
    score = models.IntegerField(null=True)


class ArticleLikes(models.Model):
    """
    Class Implementing The Article Likes Model.
    """

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=True,
        related_name='article_likes')
    article_like = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ArticleDisLikes(models.Model):
    """
    Class Implementing The Article Likes Model.
    """
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=True)
    article_dislike = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Favourites(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(
        Article, related_name="article_id",
        on_delete=models.CASCADE, null=True)
    favourite = models.BooleanField(default=False)


class Bookmark(models.Model):
    """
    Class Implementing The Bookmark Model.
    """
    reader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ReportArticle(models.Model):
    """
    Model for reporting article
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
