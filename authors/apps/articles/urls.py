from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateArticleAPIView, RetrieveArticleAPIView


urlpatterns = [
    path('articles/', CreateArticleAPIView.as_view(), name="create_article"),
    path('articles/<slug>/', RetrieveArticleAPIView.as_view(), name="detail"),

]
