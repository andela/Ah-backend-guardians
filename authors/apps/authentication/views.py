from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView

from social_django.utils import load_backend, load_strategy
from social.exceptions import AuthAlreadyAssociated
from social_core.exceptions import MissingBackend
import facebook
import os
import uuid
import twitter
from google.oauth2 import id_token
from google.auth.transport import requests
# from django.template.defaultfilters import slugify

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
    ResetPasswordSerializer, ResetPasswordConfirmSerializer,
    SocialAuthenticationSerializer
)

from .models import User


class RegistrationAPIView(GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """Method to handle post request requests for user registration

        :params:

        request - this holds the request that a user is trying to send
                  to the server.

        :returns:

        username: this holds the username that the user just registered.

        email: this holds the email that the user just registered.

        token: this holds the JWT that the user uses to access protected
                endpoints in the application.
        """

        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        valid_user = serializer.save()

        user_token = User.generate_token(user)
        current_site = get_current_site(request)
        response_data = self.send_notification(current_site,
                                               valid_user, user_token)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def send_notification(self, current_site, user, token):
        domain = f'http://{current_site.domain}'
        uid = urlsafe_base64_encode(force_bytes(user.username)).decode('utf-8')
        route = reverse('authentication:confirm', args=[token, uid])
        url = f'{domain}{route}'
        subject = "Activate your Author's Haven Account."
        message = f'Click Link Below To Activate Your Account\n{url}'
        to_email = user.email
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email,
                  [to_email], fail_silently=False)
        response_data = {
            "msg": "Go to your email address to confirm registration",
            "route": route,
        }
        return response_data


class ActivateAccountView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get(self, request, token, uid):
        try:
            username = urlsafe_base64_decode(uid).decode('utf-8')
            user = User.objects.filter(username=username).first()
        except:
            user = None
        if user is not None and not user.email_verified and \
                user.decode_token(token):
            user.email_verified = True
            user.save()
            response_data = {
                "msg": "Your account has been activated, congratulations",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        error_msg = {"error": {"detail": 'Activation link is invalid!'}}
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request, **kwargs):
        slug = kwargs['slug'].split('-')[2]
        return redirect('https://ah-frontend-guardians.herokuapp.com/reset-password/', slug)

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


class FacebookAPIView(CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = SocialAuthenticationSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get('access_token')

        try:
            """ Get user information from access token"""
            fb_user = facebook.GraphAPI(access_token=access_token)
            user_info = fb_user.get_object(
                id='me',
                fields='name, id, email')
        except:
            return Response({
                "error": "This token is invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            """ User authentication using email address """
            user = User.objects.get(email=user_info.get('email'))
            user_dict = {
                "email": user.email,
            }
            token = user.generate_token(user_dict)
            password = User.objects.make_random_password()
            return Response({
                'email': user.email,
                'username': user.username,
                'token': token
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            """ Create user if doesn't exist """
            user_dict = {
                "email": user_info.get('email')}
            password = User.objects.make_random_password()
            user = User(
                username=user_info.get('name')+str(uuid.uuid1().int)[:3],
                email=user_info.get('email'),
                is_active=1,
            )
            user.set_password(password)
            user.save()
            return Response({
                'email': user.email,
                'username': user.username,
                'token': user.generate_token(user_dict)
            }, status=status.HTTP_201_CREATED)


class GoogleAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SocialAuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get('access_token')

        try:
            """ Get user information from token"""
            user_info = id_token.verify_oauth2_token(
                access_token, requests.Request())

        except:
            return Response({
                "error": "Token-Id is invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            """ User authentication using email address if exists"""
            user = User.objects.get(email=user_info.get('email'))
            user_dict = {
                "email": user.email,
            }
            return Response({
                'email': user.email,
                'username': user.username,
                'token': user.generate_token(user_dict)
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            """ Create user if doesn't exist """
            user_dict = {
                "email": user_info.get('email')}
            password = User.objects.make_random_password()
            user = User(
                username=user_info.get('name')+"-"+str(uuid.uuid1().int)[:3],
                email=user_info.get('email'),
                is_active=1
            )
            user.set_password(password)
            user.save()
            return Response({
                'email': user.email,
                'username': user.username,
                'token': user.generate_token(user_dict)
            }, status=status.HTTP_201_CREATED)

class TwitterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SocialAuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token_key = request.data.get('access_token')
        access_token_secret = request.data.get('access_token_secret')
        try:
            consumer_key = settings.TWITTER_CONSUMER_KEY
            consumer_secret = settings.TWITTER_CONSUMER_SECRET
            api = twitter.Api(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )
            user_info = api.VerifyCredentials(include_email=True)
            user_info = user_info.__dict__
        except:
            return Response({
                "error": "This token is invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            """ User authentication using email address """
            user = User.objects.get(email=user_info.get('email'))
            user_dict = {
                "email": user.email,
            }
            return Response({
                'email': user.email,
                'username': user.username,
                'token': user.generate_token(user_dict)
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            """ Create user if doesn't exist """
            password = User.objects.make_random_password()
            user_dict = {
                "email": user_info.get('email')}
            user = User(
                username=user_info.get('name')+"-"+str(uuid.uuid1().int)[:3],
                email=user_info.get('email'),
                is_active=1,
            )
            user.set_password(password)
            user.save()
            return Response({
                'email': user.email,
                'username': user.username,
                'token': user.generate_token(user_dict)
            }, status=status.HTTP_201_CREATED)
