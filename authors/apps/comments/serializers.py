from rest_framework import serializers

from .models import Comment, LikeComment, EditHistory


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'parent', 'body',
                  'created_at', 'updated_at', 'article')
        model = Comment


class LikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'comment', 'user')
        model = LikeComment


class CommentHistorySerializer(serializers.ModelSerializer):
    """
    Class Handling History of Comment Edited
    """

    class Meta:
        model = EditHistory
        fields = ('id', 'body', 'created_at', 'user')
