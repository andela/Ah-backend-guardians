import json
from rest_framework.test import APIClient
from rest_framework.views import status
from authors.apps.authentication.tests.data import login_info
from authors.apps.authentication.tests.base import BaseTestCase
from django.urls import reverse
from ..models import Article


class TestFavouriteArticle(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.article = {

            "title": "My Best Day In 2018",
            "body": "It was on 16th Jan when I had my graduation",
            "description": "Graduation Day"
        }
        self.url = reverse('article:create_article')

    def create_article(self):
        login_user = self.log_in_user(login_info)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + login_user.data['token'])
        response = self.client.post(
            self.url, data=self.article, format='json')
        return response.data['slug']

    def get_user_token(self):
        request = self.log_in_user(login_info)
        return request.data['token']

    def test_favourite_article(self):
        """
        Test For User To Favorite Article
        """
        login_user = self.log_in_user(login_info)
        slug = self.create_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + login_user.data['token'])
        response = self.client.put(
            self.url+slug+'/favorite/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("{'article': {'message': 'article has been favorited'}}",
                      str(json.loads(response.content)))

    def test_unfavourite_article(self):
        login_user = self.log_in_user(login_info)
        slug = self.create_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + login_user.data['token'])
        self.client.put(
            self.url+slug+'/favorite/',
            data=self.article,
            format='json'
        )
        response = self.client.put(
            self.url+slug+'/favorite/',
            data=self.article,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "{'article': {'message': 'article has been unfavorited'}}",
            str(json.loads(response.content))
        )

    def test_get_article(self):
        login_user = self.log_in_user(login_info)
        slug = self.create_article()
        self.client.post(reverse('article:create_article'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        article = Article.objects.latest('created_at').slug
        self.client.put(f'/api/articles/{article}/favorite/',
                        HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.get(f'/api/favorites/',
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.get_user_token())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
