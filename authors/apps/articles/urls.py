from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateArticleAPIView, RetrieveArticleAPIView, \
                    CreateRatingsView


urlpatterns = [
    path('articles/', CreateArticleAPIView.as_view(), name="create_article"),
    path('articles/<slug>/', RetrieveArticleAPIView.as_view(), name="detail"),
    path('articles/<slug>/rating/', CreateRatingsView.as_view(),
         name="ratings_list"),
    path('articles/<slug>/rating/<article_id>', CreateRatingsView.as_view(),
         name="ratings_list_id"),
]
