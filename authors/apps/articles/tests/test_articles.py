from django.test import TestCase
from rest_framework import status
from rest_framework.utils.serializer_helpers import OrderedDict
from rest_framework.test import APITestCase, APIClient
from authors.apps.authentication.tests.base import BaseTestCase
from django.urls import reverse
from django.conf import settings

from authors.apps.authentication.tests.data import login_info
from ..models import Article
from .data import article_body
from authors.apps.authentication.models import User
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory
)


class TestArticle(BaseTestCase):

    def setUp(self):
        self.client = APIClient()
        self.article = {

            "title": "My Best Day In 2018",
            "body": "It was on 16th Jan when I had my graduation",
            "description": "Graduation Day"
        }
        self.update_data = {

            "title": "My Best Day In 2019",
            "body": "It was on 16th Jan when I had my graduation",
            "description": "Graduation Day"

        }
        self.url = reverse('article:create_article')

    def get_user_token(self):
        data1 = {
            'email': 'moses@gmail.com',
            'username': 'moses',
            'password': 'Kamira123'
        }
        data2 = {
            'email': 'moses@gmail.com',
            'password': 'Kamira123'
        }
        request = self.log_in_user(login_info)
        return request.data['token']

    def test_create_article_forbidden(self):
        res = self.client.post(
            self.url, self.article, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_models_article(self):
        """Test if the article has a read time"""
        user = User.objects.create_user(
            username='moses', email='moses@gmail.com',
            password='Kamira123')
        user.is_verified = True
        user = User.objects.filter(email='moses@gmail.com').first()
        author = user
        article = Article.objects.create(
            title='article title', author=author)
        self.assertEqual(str(article), article.title)

    def test_check_read_time(self):
        user = User.objects.create_user(
            username='moses', email='moses@gmail.com',
            password='Kamira123')
        user.is_verified = True
        user = User.objects.filter(email='moses@gmail.com').first()
        author = user
        article = Article.objects.create(
            title='article title', body=article_body, author=author)
        number_of_words = Article.count_words(article.body)
        reading_time = int(number_of_words/settings.WPM)
        self.assertEqual(article.read_time, reading_time)

    def test_create_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        get_response = self.client.get(self.url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_get_article_doesnot_exist(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        get_response = self.client.get(
            self.url + 'mose/', format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_response.data['error'], 'Article does not exist')

    def test_delete_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        res = self.client.delete(
            self.url+slug+'/',  format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
