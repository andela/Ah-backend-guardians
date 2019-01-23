from django.urls import reverse

from rest_framework.views import status

from .base import BaseTestCase
from .data import login_info, login_info2
from authors.apps.comments.models import LikeComment


class LikeCommentTest(BaseTestCase):

    def setUp(self):
        response = self.log_in_user(login_info)
        self.token = response.data['token']

        response2 = self.log_in_user(login_info2)
        self.token2 = response2.data['token']

        self.slug = 'code'
        self.id = 1
        self.pk = 1
        self.url = reverse('comments:like_comment', args=[self.slug, self.id])
        self.url2 = reverse('comments:like_comment', args=[self.slug, 0])
        self.url3 = reverse('comments:retrieve_comment',
                            args=[self.slug, self.id, self.pk])

    def test_like_comment(self):
        '''Tests authenticated users can like comments'''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.put(self.url)
        like = LikeComment.objects.all().filter(comment=self.id, user=3)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like)

    def test_unlike_comment(self):
        '''Tests authenticated users can like comments'''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(self.url)
        like = LikeComment.objects.all().filter(comment=self.id, user=2)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertFalse(like)

    def test_get_all_likes_for_comment(self):
        '''Tests authenticated users can view all the likes of a comment'''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_like_non_existant_comment(self):
        '''Tests that users cannot like a comment that doesn't exist'''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
