from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance to JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Article
        fields = ('id', 'title', 'body', 'description','slug'
                  'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
