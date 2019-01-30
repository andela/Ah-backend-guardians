from django.urls import reverse
from rest_framework import status
from ..models import EditHistory
from .data import login_info, comment2
from .base import BaseTestCase


class TestCommentHistory(BaseTestCase):
    """
    This class tests the functions for editing
    comment and viewing history of edited comment
    """

    def setUp(self):
        response = self.log_in_user(login_info)
        self.token = response.data['token']
        self.slug = 'code'
        self.id = 2
        self.url1 = reverse("comments:specific_comment",
                            args=[self.slug, self.id])
        self.url2 = reverse("comments:comment_history",
                            args=[self.slug, self.id])
        self.url3 = reverse("comments:comment_history",
                            args=[self.slug, 15])

    def test_get_comment_edit_history(self):
        """Test to get all edited comments"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response1 = self.client.put(self.url1, comment2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.get(self.url2)
        history = EditHistory.objects.get(comment=self.id)
        self.assertTrue(str(history))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data[0]['body'], history.body)

    def test_get_comment_edit_history_not_exist(self):
        """Test to get edit history does not exist"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response2 = self.client.get(self.url2)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response2.data['message'],
            "No Edit History For To This Comment")

    def test_comment_does_not_exist(self):
        """Testing that the Comment does not exist"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(
            reverse("comments:specific_comment", args=['code', 0]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
