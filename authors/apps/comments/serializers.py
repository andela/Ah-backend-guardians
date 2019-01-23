from rest_framework import serializers

from authors.apps.authentication.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'parent', 'body',
                  'created_at', 'updated_at', 'article')
        model = Comment
