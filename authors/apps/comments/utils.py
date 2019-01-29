from rest_framework.exceptions import NotFound

from .models import Comment
from authors.apps.articles.models import Article
from rest_framework import serializers


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

    def check_index(self, index, article_length):
        if not index:
            return None
        if index > article_length:
            raise serializers.ValidationError(
                "Index should be less than %s" % (article_length))
        return index

    def comment_on_selected(self, start_index, end_index, article):
        article_length = len(article.body)
        start_index = self.check_index(
            start_index, article_length)
        end_index = self.check_index(
            end_index, article_length)
        if start_index and end_index:
            text = [start_index, end_index] if start_index < end_index else [
                end_index, start_index]
            selected_text = str(article.body[text[0]:text[1]])
            return selected_text
