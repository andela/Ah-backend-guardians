import uuid
import jwt
from django.shortcuts import render
from django.template.defaultfilters import slugify
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer, ArticlesLikesJSONRenderer
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status, filters
from .models import Article, Rating, ArticleLikes, ArticleDisLikes
from authors import settings
from .filters import ArticleFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .serializers import (
    CreateArticleAPIViewSerializer, RatingSerializer, LikeArticleSerializer, DisLikeArticleSerializer
)
from authors.settings import RPD
from ..authentication.models import User
from rest_framework.pagination import LimitOffsetPagination
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import Article
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from authors.apps.articles.filters import ArticleFilter


class CreateArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticlesJSONRenderer, )
    queryset = Article.objects.all()
    serializer_class = CreateArticleAPIViewSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10
    pagination_class.offset_query_param = 'page'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = ArticleFilter
    search_fields = ('title', 'body', 'description',
                     'tags', 'author__username')

    def post(self, request):
        """ Method For Posting Article """
        article = request.data

        serializer = self.serializer_class(
            data=article, context={'request': request})
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
            serializer = self.serializer_class(
                article, context={'request': request})
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


class LikeArticleStatus(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticlesLikesJSONRenderer,)
    serializer_class = LikeArticleSerializer
    queryset = ArticleLikes.objects.all()

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        article_like = ArticleLikes.objects.filter(
            article__slug=slug, user=self.request.user).first()
        if article_like:
            return article_like


class DisLikeArticleStatus(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticlesLikesJSONRenderer,)
    serializer_class = DisLikeArticleSerializer

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        article_dislikes = ArticleDisLikes.objects.filter(
            article__slug=slug, user=self.request.user).first()
        if article_dislikes:
            return article_dislikes


class LikeArticleAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ArticleLikes.objects.all()

    def get_object(self):
        """Method to get an article"""
        slug = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug)

    def get_queryset(self, request):
        """Method to get liked or disliked articles"""
        article = self.get_object()
        liked_article = self.queryset.filter(
            article=article, user=request.user).first()
        return liked_article

    def like_response_message(self, message):
        return Response(message, status=status.HTTP_200_OK)

    def put(self, request, slug):
        """
        Updates the article with the reader's like choice
        params:
        request, 
        slug param

        Returns:
        HTTP Response
        HTTP Status code
        """
        user = request.user
        article = self.get_object()
        liked_article = self.get_queryset(request)
        disliked_article = ArticleDisLikes.objects.filter(
            article=article, user=request.user).first()
        like_status = [{"message": "liked"}, {"message": "unliked"}]

        if not liked_article:
            if disliked_article:
                disliked_article.delete()

                article_likes = ArticleLikes.objects.create(
                    article=article, user=user, article_like=True)
                article_likes.save()
                return self.like_response_message(like_status[0])
            article_likes = ArticleLikes.objects.create(
                article=article, user=user, article_like=True)
            article_likes.save()
            return self.like_response_message(like_status[0])

        else:
            if liked_article.article_like:
                liked_article.article_like = False
                liked_article.save()
                return self.like_response_message(like_status[1])
            else:
                liked_article.article_like = True
                liked_article.save()
                return self.like_response_message(like_status[0])


class DisLikeArticleAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ArticleDisLikes.objects.all()

    def get_object(self):
        """Method to get an article"""
        slug = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug)

    def get_queryset(self, request):
        """Method to get liked or disliked articles"""
        article = self.get_object()
        disliked_article = self.queryset.filter(
            article=article, user=request.user).first()
        return disliked_article

    def dislike_response_message(self, message):
        return Response(message, status=status.HTTP_200_OK)

    def put(self, request, slug):
        """
        Updates the article with the reader's like choice
        params:
        request, 
        slug param

        Returns:
        HTTP Response
        HTTP Status code
        """
        user = request.user
        article = self.get_object()
        disliked_article = self.get_queryset(request)
        liked_article = ArticleLikes.objects.filter(
            article=article, user=request.user).first()
        dislike_status = [{"message": "disliked"}, {"message": "undisliked"}]

        if not disliked_article:
            if liked_article:
                liked_article.delete()
                article_dislikes = ArticleDisLikes.objects.create(
                    article=article, user=user, article_dislike=True)
                article_dislikes.save()
                return self.dislike_response_message(dislike_status[0])
            article_dislikes = ArticleDisLikes.objects.create(
                article=article, user=user, article_dislike=True)
            article_dislikes.save()
            return self.dislike_response_message(dislike_status[0])

        else:
            if disliked_article.article_dislike:
                disliked_article.article_dislike = False
                disliked_article.save()
                return self.dislike_response_message(dislike_status[1])
            else:
                disliked_article.article_dislike = True
                disliked_article.save()
                return self.dislike_response_message(dislike_status[0])
