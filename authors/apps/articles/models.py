from django.db import models
from datetime import datetime, timedelta
from ..authentication.models import User
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


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
                      blank=True), unique=False, blank=True, default=list)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]

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
