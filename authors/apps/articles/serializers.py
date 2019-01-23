
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status, exceptions
from ..authentication.serializers import UserSerializer
from .models import Article, ArticleLikes


class CreateArticleAPIViewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'description',
                  'author', 'slug', 'published', 'created_at',
                  'updated_at', 'images', 'read_time', 'tags',
                  'likes_count', 'dislikes_count')

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


class LikeArticleAPIViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleLikes
        fields = ['user', 'article', 'article_like']
