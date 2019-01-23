from rest_framework.exceptions import NotFound

from .models import Comment
from authors.apps.articles.models import Article


class Utils:
    def check_article(self, slug):
        try:
            article = Article.objects.get(slug=slug)
            return article
        except Article.DoesNotExist:
            raise NotFound(
                {'error': 'Article with slug: %s does not exist' % (slug)})

    def check_comment(self, id):
        try:
            comment = Comment.objects.get(pk=id)
            return comment
        except Comment.DoesNotExist:
            raise NotFound(
                {'error':
                 'Comment with id: %d does not exist for this article' % (id)})
