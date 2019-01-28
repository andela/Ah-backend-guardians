import uuid
import jwt
from django.shortcuts import render
from django.template.defaultfilters import slugify
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from .models import Article, Rating
from authors import settings


from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .serializers import (
    CreateArticleAPIViewSerializer, RatingSerializer
)
from authors.settings import RPD
from ..authentication.models import User
from .models import Article
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination


class CreateArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticlesJSONRenderer,)
    queryset = Article.objects.all()
    serializer_class = CreateArticleAPIViewSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10
    pagination_class.offset_query_param = 'page'

    def post(self, request):
        """ Method For Posting Article """
        article = request.data

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        response = serializer.data

        response.update(article)

        return Response(response, status=status.HTTP_201_CREATED)


class RetrieveArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = CreateArticleAPIViewSerializer
    queryset = Article.objects.all()

    def retrieve(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            response = {
                'error': 'Article does not exist'
            }
            return Response(response, status.HTTP_404_NOT_FOUND)

    def update(self, request, slug):
        """This method updates a user article"""

        article = request.data.get('article', {})
        article["author"] = request.user.email

        article_instance = Article.objects.get(slug=slug)

        slug = slugify(request.data.get("article")['title'].replace("_", "-"))
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        if article_instance.author != request.user:

            raise PermissionDenied

        serializer = self.serializer_class(
            article_instance, data=article, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        data = serializer.data

        data["message"] = "Article updated successfully."
        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, slug):
        """This method allows a user to delete his article"""
        article_instance = get_object_or_404(Article, slug=slug)
        if article_instance.author != request.user:
            raise PermissionDenied
        self.perform_destroy(article_instance)
        return Response(
            {"message": "Article is deleted"},
            status=status.HTTP_200_OK
        )


class CreateRatingsView(generics.UpdateAPIView):
    """
    Class to handle the rating of articles
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ArticleJSONRenderer,)

    def get_queryset(self, data, user, slug):
        """
        Method to get the article slug and compare it with
        available slugs in the database. It shall also handle all
        permissions in relation to rating an article
        """
        article = get_object_or_404(Article, slug=slug)
        if article.author == self.request.user:
            raise PermissionDenied({"error":
                                    "You cannot rate an article you created"})
        if Rating.objects.filter(
                reader=user.pk).filter(article=article.id).exists():
            raise ParseError({"error": "You already rated this article"})

        data.update({"article": article.pk})
        data.update({"reader": user.pk})
        return data

    def put(self, request, slug=None):
        """
        Method that edit a rating for an article provided, check whether
        it meets the correct criteria and if it does not, the appropriate
        error message is returned
        """

        data = self.get_queryset(
            request.data, request.user, slug)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
