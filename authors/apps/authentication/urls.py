from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

schema_view = get_swagger_view(title='Login API')

urlpatterns = [
    url(r'swagger-docs/', schema_view),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
]
