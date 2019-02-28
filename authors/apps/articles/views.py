from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, exceptions, generics
from .models import (Article, Favourites, Rating,
                     ArticleLikes, ArticleDisLikes, Bookmark)
from ..authentication.models import User
from authors.apps.profiles.models import ReadingStat
from .serializers import (
    CreateArticleAPIViewSerializer, RatingSerializer, LikeArticleSerializer,
    DisLikeArticleSerializer, FavouriteSerializer, BookmarkSerializer
)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.generics import get_object_or_404, GenericAPIView
from authors import settings

import uuid
import jwt

from django.shortcuts import render
from django.template.defaultfilters import slugify

from rest_framework.exceptions import (
    PermissionDenied, ParseError, NotFound, ValidationError)
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.response import Response

from authors.settings import RPD
from .renderers import (ArticleJSONRenderer, ArticlesJSONRenderer,
                        ArticlesLikesJSONRenderer, BookmarksJSONRenderer)


class CreateArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticlesJSONRenderer, )
    queryset = Article.objects.all()
    serializer_class = CreateArticleAPIViewSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10
    pagination_class.offset_query_param = 'page'

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
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = CreateArticleAPIViewSerializer
    queryset = Article.objects.all()

    def retrieve(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            serializer = self.serializer_class(
                article, context={'request': request})
            logged_in = request.user.is_authenticated
            if logged_in and article.author.pk != request.user.pk:
                ReadingStat.objects.get_or_create(
                    user=request.user, articles=article)
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
            article_instance,
            data=article,
            context={'request': request},
            partial=True)

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


class RetrieveMyArticles(generics.ListAPIView):
    serializer_class = CreateArticleAPIViewSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ArticlesJSONRenderer,)
    queryset = Article.objects.all()
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10
    pagination_class.offset_query_param = 'page'

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(author=self.request.user)


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


class FavouritesView(GenericAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)

    def get_object(self, **kwargs):
        article_slug = self.kwargs.get('slug')
        article_obj = get_object_or_404(Article, slug=article_slug)
        return article_obj

    def put(self, request, **kwargs):
        article = self.get_object()
        user = request.user
        article_id = article.id
        fav = Favourites.objects.filter(
            article_id=article_id, user=user
        ).first()
        if fav:
            current_count = article.favouriteCount
            if fav.favourite:
                if current_count == 1:
                    article.favorited = False
                fav.favourite = False
                article.favouriteCount = current_count - 1
                response_data = {
                    "message": "article has been unfavorited"
                }
            else:
                fav.favourite = True
                article.favouriteCount = current_count + 1
                response_data = {
                    "message": "article has been favorited"
                }
            fav.save()
            article.save()
            return Response(response_data, status=200)

        else:
            serializer = self.serializer_class(data={}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user,
                            article=article, favourite=True)

            article.favouriteCount = article.favouriteCount + 1
            article.favorited = True
            article.save()

            return Response({"message": "article has been favorited"
                             }, status=200)

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Favourites.objects.filter(favourite=True, user=user)

        serializer = FavouriteSerializer(
            queryset, many=True, context={'request': request})

        if not serializer.data:
            return Response({
                "message": "No Article Favorited Yet"
            },
                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateBookmarkArticleView(generics.CreateAPIView):
    """
    Class to handle the bookmarking of an articles
    """
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Bookmark.objects.all()
    renderer_classes = (BookmarksJSONRenderer,)

    def get_object(self, slug):
        try:
            article = Article.objects.get(slug=slug)
            return article
        except Article.DoesNotExist:
            raise NotFound(
                {'error': 'Article  your trying to '
                          'bookmark does not exist'})

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        article = self.get_object(slug)
        title = article.title
        bookmark = self.get_queryset().filter(reader=self.request.user,
                                              article=article)
        if bookmark:
            raise PermissionDenied(
                {"error": "You cannot bookmark"
                 "your own article"})
        bookmark = Bookmark.objects.create(
            article=article, reader=request.user)
        serializer = self.serializer_class(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListBookmarksView(generics.ListAPIView):
    """
    Class to list all bookmarks
    """
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Bookmark.objects.all()
    renderer_classes = (BookmarksJSONRenderer,)

    def get_queryset(self):
        return self.queryset.filter(reader=self.request.user)


class RetrieveDeleteBoomarkView(generics.RetrieveDestroyAPIView):
    """
    Class to delete or retrieve a bookmark
    """
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BookmarksJSONRenderer,)

    def get_object(self):
        article_slug = self.kwargs.get('slug')
        try:
            article = Article.objects.get(slug=article_slug)
            bookmark = Bookmark.objects.get(article=article)
            if bookmark.reader != self.request.user:
                raise PermissionDenied(
                    {"error": "You do not have permission to "
                              "perform this action."})
        except Article.DoesNotExist:
            raise NotFound(
                {'error': 'Bookmark does not exist'})
        except Bookmark.DoesNotExist:
            raise NotFound(
                {'error': 'Bookmark does not exist'})
        return bookmark

    def delete(self, request, *args, **kwargs):
        bookmark = self.get_object()
        if bookmark:
            bookmark.delete()
            return Response(
                {"message": f"You have unbookmarked the "
                            f"article"},
                status=status.HTTP_200_OK
            )
