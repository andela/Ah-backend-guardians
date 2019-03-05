from .models import Article
import django_filters
from django_filters import FilterSet, rest_framework as filters


class ArticleFilter(FilterSet):
    """
    Method that handles filtering of data by a particular
    parameter
    """
    title = filters.CharFilter(lookup_expr='icontains')
    tags = filters.CharFilter(method='tag_filter')
    author = filters.CharFilter('author__username',
                                lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['title', 'author', 'tags']

    def tag_filter(self, queryset, key, value):
        return queryset.filter(tags__icontains=value)
