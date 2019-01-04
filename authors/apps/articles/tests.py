from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Article
from .serializers import ArticleSerializer
from django.conf import settings
import json

class ArticleTests(APITestCase):
    def test_create_article(self):
        """
        Ensure we can create a new article object.
        """
        url = reverse('articles:create')
        data = {'title':'Why Python is great','body':'some text...'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       
    def test_get_article(self):
        """
        Ensure we can get an article object.
        """
        url = reverse('articles:create')
        data = {'title':'Why Python is great','body':'some text...'}
        response = self.client.post(url, data, format='json')
        url2 = reverse('articles:create')
        response2 = self.client.get(url, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)




