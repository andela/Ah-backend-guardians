import uuid
import jwt
from django.shortcuts import render
from django.template.defaultfilters import slugify
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework import generics, status
from .models import Article, Favourites
from authors import settings
from ..authentication.backends import JWTAuthentication


from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .serializers import (
    CreateArticleAPIViewSerializer, FavouriteSerializer
)
from authors.settings import RPD
from ..authentication.models import User
from .models import Article
from rest_framework import generics


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


class FavouritesView(GenericAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)

    def post(self, request, **kwargs):
        user = request.user
        user_id = user.pk
        article_slug = kwargs['slug']
        article_obj = Article.objects.get(slug=article_slug)
        article_id = article_obj.id
        fav = Favourites.objects.filter(
            article_id=article_id
        ).filter(
            user=user
        )

        fav_option = fav.first()
        if fav_option:
            return Response(
                {
                    "error": {
                        "body": [
                            "article already favorited"
                        ]
                    }
                },
                status=409
            )
        else:

            serializer = self.serializer_class(data={}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user,
                            article=article_obj, favourite=True)

            favs = Favourites.objects.filter(
                article_id=article_id,
                favourite=True
            )

            article_obj.favourited = True
            article_obj.favouriteCount = favs.count()
            article_obj.save()
            return Response(serializer.data, status=200)

    def put(self, request, **kwargs):
        user = request.user
        article_slug = kwargs['slug']
        article_obj = Article.objects.get(slug=article_slug)
        article_id = article_obj.id
        fav = Favourites.objects.filter(
            article_id=article_id
        ).filter(
            user=user
        ).filter(
            favourite=True
        )
        fav.delete()
        counter = article_obj.favouriteCount
        if (counter == 1):
            article_obj.favourited = False

        if (counter >= 1):
            article_obj.favouriteCount = counter - 1
        article_obj.save()
        serializer = self.serializer_class(data={}, partial=True)
        serializer.is_valid(raise_exception=True)

        return Response({

            "message": [
                "article has been unfavorited"
            ]

        }, status=200)
