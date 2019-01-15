from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

from .models import User
import jwt
from datetime import datetime, timedelta
from django.conf import settings

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetPasswordSerializer, ResetPasswordConfirmSerializer
)


class RegistrationAPIView(GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """Method to handle post request requests for user registration

        :params:

        request - this holds the request that a user is trying to send to the server.

        :returns:

        username: this holds the username that the user just registered.

        email: this holds the email that the user just registered.

        token: this holds the JWT that the user uses to access protected endpoints in the application.
        """

        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_token = User.generate_token(user)

        response_data = {'username': user['username'], 'token': user_token}
        response_data.update(serializer.data)

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_token = User.generate_token(user)

        response_data = {'username': user['email'], 'token': user_token}
        response_data.update(serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    @classmethod
    def decode_id(self, uid):
        username = urlsafe_base64_decode(uid).decode('utf-8')
        return username

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=user['email']).first()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.username)).decode('utf-8')
        domain = 'http://{}'.format(get_current_site(request))
        route = 'api/password-reset-confirm/'
        url = '{}/{}{}-{}'.format(domain, route, token, uid)
        subject = 'Authors Haven: Have Your Password Changed'
        message = 'Follow The Link Below To Reset Your Password {}'.format(url)
        email_from = settings.EMAIL_HOST_USER
        to_mail = user.email
        recipient_list = [to_mail]
        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False
        )
        res = {"message": "An Email Has Been Sent To This Email Address"}
        return Response(res, status.HTTP_200_OK)


class ResetPasswordConfirmAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordConfirmSerializer

    def get_object(self):
        return {"password": "", "confirm_password": ""}

    def update(self, request, **kwargs):
        serializer_data = request.data
        slug = kwargs['slug'].split('-')[2]
        user = ResetPasswordAPIView().decode_id(slug)
        if serializer_data['password'] == serializer_data['confirm_password']:
            serializer = self.serializer_class(
                request.data, data=serializer_data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            new_password = make_password(serializer_data['confirm_password'])
            User.objects.filter(username=user).update(password=new_password)

            return Response({
                "message": {
                    "detail": [
                        "Password Has Been Successfully Reset, Please Login "
                    ]
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "errors": {
                "body": [
                    "Password Mismatch, Please Re-enter Password"
                ]
            }
        }, status=status.HTTP_400_BAD_REQUEST)
