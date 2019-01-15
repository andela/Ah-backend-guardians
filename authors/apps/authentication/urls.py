from django.urls import path
from django.contrib.auth import views as auth_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ResetPasswordAPIView, ResetPasswordConfirmAPIView,
)

schema_view = get_schema_view(
    openapi.Info(
        title=" Authors Haven",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="detail"),
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('password-reset/', ResetPasswordAPIView.as_view()),
    path('password-reset-confirm/<slug>', ResetPasswordConfirmAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0),
         name='schema-swagger-ui'),
]
