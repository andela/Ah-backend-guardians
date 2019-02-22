from django.urls import reverse

from .data import article
from .base import BaseTestCase
from rest_framework.views import status

from .data import (login_info, login_info2, article_2,
                   highlight_forward, highlight_backward,
                   highlight_out_index)
from authors.apps.authentication.models import User


class TestHighlightCommentArticle(BaseTestCase):
    def setUp(self):
        login_one = self.log_in_user(login_info)
        self.token1 = login_one.data['token']
        login_two = self.log_in_user(login_info2)
        self.token2 = login_two.data['token']
        article_url = reverse('article:create_article')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        self.client.post(article_url, article_2, format='json')
        slug = 'article-2'
        self.url = reverse("comments:comment", args=[slug])

    def test_comment_on_article_forward_index(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.post(self.url, highlight_forward, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         'Comment Successfully added')

    def test_comment_on_article_backward_index(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.post(
            self.url, highlight_backward, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         'Comment Successfully added')

    def test_comment_on_article_out_side_index(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.post(
            self.url, highlight_out_index, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Index should be less than 554", response.data['errors'])

    def test_comment_on_article_with_negative_end_index(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        highlight_forward["end_index"] = -40
        response = self.client.post(
            self.url, highlight_forward, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_on_article_with_negative_start_index(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        highlight_forward["start_index"] = -60
        response = self.client.post(
            self.url, highlight_forward, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
