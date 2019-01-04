from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

schema_view = get_swagger_view(title='Users API')


urlpatterns = [
    path('swagger-docs/', schema_view),
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('users/', RegistrationAPIView.as_view(), name='users'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
]
