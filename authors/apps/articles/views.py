import uuid
import jwt
from django.shortcuts import render
from django.template.defaultfilters import slugify
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from .models import Article, ArticleLikes
from authors import settings


from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .serializers import (
    CreateArticleAPIViewSerializer, LikeArticleAPIViewSerializer
)
from authors.settings import RPD
from ..authentication.models import User
from .models import Article
from rest_framework import generics
from ..authentication.backends import JWTAuthentication


class CreateArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticlesJSONRenderer,)
    queryset = Article.objects.all()
    serializer_class = CreateArticleAPIViewSerializer

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


class LikeArticleAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = LikeArticleAPIViewSerializer
    queryset = ArticleLikes.objects.all()

    def put(self, request, slug):
        user = request.user
        try:
            article = Article.objects.all().filter(slug=slug).first()
            liked_article = self.queryset.filter(
                article=article, user=user).first()
            if liked_article.article_like is True:
                liked_article.article_like = False
                liked_article.save()
                return Response({"message": "disliked"},
                                status=status.HTTP_200_OK)
            liked_article.article_like = True
            liked_article.save()
            return Response({"message": "liked"},
                            status=status.HTTP_200_OK)
        except:
            if article is not None:
                article_likes = ArticleLikes.objects.create(
                    article=article, user=user, article_like=True)
                article_likes.save()
                return Response({"message": "liked"},
                                status=status.HTTP_200_OK)
            response = {
                'error': 'You can not like an article that does not exist'
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
