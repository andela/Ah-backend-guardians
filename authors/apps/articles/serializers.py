from urllib.parse import quote

from django.urls import reverse

from rest_framework import serializers
from ..authentication.serializers import UserSerializer
from .models import (Article, Rating, ArticleLikes,
                     ArticleDisLikes, Favourites, Bookmark,
                     ReportArticle)
from ..authentication.models import User
from ..authentication.serializers import UserSerializer


class CreateArticleAPIViewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'description',
                  'author', 'slug', 'published', 'created_at',
                  'updated_at', 'images', 'read_time', 'tags',
                  'average_rating', 'social_links', 'likes_count',
                  'dislikes_count', 'favourited',
                  'favouriteCount')

    def validate_title(self, value):
        if len(value) > 255:
            raise serializers.ValidationError(
                'The title should not be more than 255 characters'
            )
        return value

    def validate_description(self, value):
        if len(value) > 255:
            raise serializers.ValidationError(
                'The article should not be more than 255 characters'
            )
        return value

    def get_social_links(self, obj):
        social_links = dict()
        article_url = self.context['request'].build_absolute_uri(
            reverse("article:detail", args=[obj.slug]))
        share_string = quote(article_url)
        # generating facebook links
        facebook_url = f"https://www.facebook.com/sharer/s" \
            f"harer.php?u={share_string}"
        social_links['facebook'] = facebook_url
        # generating twitter links
        twitter_url = f"https://twitter.com/home?status={share_string}"
        social_links['twitter'] = twitter_url
        # generating email links
        subject = quote(f"{obj.title} from Author's Haven")
        body = quote(
            f"Click Link To View The Article {article_url}")
        email_link = f'mailto:?&subject={subject}&body={body}'
        social_links['email'] = email_link
        return social_links


class RatingSerializer(serializers.ModelSerializer):

    """
    Serializer for rating an article model
    """
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all())
    score = serializers.IntegerField(
        required=True, max_value=5, min_value=1)
    reader = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Rating
        fields = ("score", "article", "reader")


class LikeArticleSerializer(serializers.ModelSerializer):

    """
    Serializer for liking an article model
    """
    class Meta:
        model = ArticleLikes
        fields = ("article_like", )


class DisLikeArticleSerializer(serializers.ModelSerializer):

    """
    Serializer for liking an article model
    """
    class Meta:
        model = ArticleDisLikes
        fields = ("article_dislike", )


class FavouriteSerializer(serializers.ModelSerializer):
    article = CreateArticleAPIViewSerializer(read_only=True)

    class Meta:
        model = Favourites
        fields = [
            'article', 'favourite', 'user'
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for bookmarking an article model
    """
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ("id", "title", "description",
                  "read_time", "author", "created_at", "reader", "slug")

    def get_title(self, obj):
        return obj.article.title

    def get_description(self, obj):
        return obj.article.description

    def get_read_time(self, obj):
        return obj.article.read_time

    def get_author(self, obj):
        return obj.article.author.username

    def get_slug(self, obj):
        return obj.article.slug

class ReportSerializer(serializers.ModelSerializer):
    """
    Report article class.
    """
    article = CreateArticleAPIViewSerializer(read_only=True)
    reported_by = UserSerializer(read_only=True)

    class Meta:
        model = ReportArticle
        fields = ("reported_by", "reason", "reported_at", "article")
