from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ResetPasswordAPIView, ResetPasswordConfirmAPIView,
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="detail"),
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('password-reset/', ResetPasswordAPIView.as_view()),
    path('password-reset-confirm/<slug>', ResetPasswordConfirmAPIView.as_view()),
]
