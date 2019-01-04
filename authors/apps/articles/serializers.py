from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance to JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        extra_kwargs = {
            'slug': {'read_only': True}
        }
        model = Article
        fields = ('id', 'title', 'body', 'description','slug','image',
                  'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
