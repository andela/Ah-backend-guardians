from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CreateArticleAPIView,
                    RetrieveArticleAPIView, LikeArticleAPIView,
                    DisLikeArticleAPIView, CreateRatingsView,
                    LikeArticleStatus, DisLikeArticleStatus, FavouritesView,
                    RetrieveMyArticles)


urlpatterns = [
    path('articles/', CreateArticleAPIView.as_view(), name="create_article"),
    path('articles/my_articles/', RetrieveMyArticles.as_view(),
         name="view_my_articles"),
    path('articles/<slug>/', RetrieveArticleAPIView.as_view(), name="detail"),
    path('articles/<slug>/rating/', CreateRatingsView.as_view(),
         name="ratings_list"),
    path('articles/<slug>/rating/<article_id>', CreateRatingsView.as_view(),
         name="ratings_list_id"),
    path('articles/<slug>/like/', LikeArticleAPIView.as_view(),
         name="like_article"),
    path('articles/<slug>/dislike/', DisLikeArticleAPIView.as_view(),
         name="dislike_article"),
    path('articles/<slug>/get_article_like/', LikeArticleStatus.as_view(),
         name="get_article_like"),
    path('articles/<slug>/get_article_dislike/',
         DisLikeArticleStatus.as_view(),
         name="get_article_dislike"),
    path('articles/<slug>/favorite/', FavouritesView.as_view()),
    path('favorites/', FavouritesView.as_view(), name="favorited_articles"),
    
]
