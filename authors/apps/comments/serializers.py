from rest_framework import serializers

from .models import Comment, LikeComment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'parent', 'body',
                  'created_at', 'updated_at', 'article')
        model = Comment


class LikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'comment', 'user')
        model = LikeComment
