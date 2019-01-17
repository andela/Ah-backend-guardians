
from django.contrib.auth import authenticate
from rest_framework import serializers
# from rest_framework import status, exceptions
from ..authentication.serializers import UserSerializer
from .models import Article, Rating
from rest_framework.exceptions import PermissionDenied
from ..authentication.models import User



class CreateArticleAPIViewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'description',
                  'author', 'slug', 'published', 'created_at',
                  'updated_at', 'images', 'read_time', 'tags','average_rating')

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

class RatingSerializer(serializers.ModelSerializer):

    """
    Serializer for rating an article model
    """
    article = serializers.PrimaryKeyRelatedField(
        queryset = Article.objects.all())
    score = serializers.IntegerField(
        required=True)
    reader = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    @staticmethod
    def update_data(data, slug, user: User):
        try:
            article = Article.objects.get(slug__exact=slug)
        except Article.DoesNotExist:
            raise NotFound({
                'error':  "Article does not exist. "
                                   "Check provided Article slug."
            })

        if article.author == user:
            raise PermissionDenied({
                "error":
                "You cannot rate an article that you created."
            })
        
        data.update({"article":article.pk})
        data.update({"reader": user.pk})
        return data

    def create(self, data):
        """
        Method that saves ratings
        """
        reader = data.get("reader")
        article = data.get("article")
        score = data.get("score")
        if score > 5 or score < 1:
            raise IncorrectValues({
                "error":
                "Score must be an integer between 1 and 5."
            })
        try:
            rating = Rating.objects.get(reader=reader,
                article__slug=article.slug)
        except Rating.DoesNotExist:
            return Rating.objects.create(**data)
        rating.score = score
        rating.save()
        return rating

    


    class Meta:
        """
        class behaviours
        """
        model = Rating
        fields = ("score","article","reader")
 