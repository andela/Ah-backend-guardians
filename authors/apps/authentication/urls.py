from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="detail"),
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
]
