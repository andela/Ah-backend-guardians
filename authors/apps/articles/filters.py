from .models import Article
import django_filters
from django_filters import FilterSet, rest_framework as filters


class ArticleFilter(django_filters.FilterSet):
    """
    Custom function that manages manages the fields we can loop 
    through to perform a search by field
    """
    title = filters.CharFilter(lookup_expr='icontains')
    tags = filters.CharFilter(method='tag_filter')

    class Meta:
        model = Article
        fields = ['title', 'author__username', 'tags']

    def tag_filter(self, queryset, key, value):
        return queryset.filter(tags__icontains=value)
