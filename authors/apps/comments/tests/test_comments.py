from django.urls import reverse

from .data import article
from .base import BaseTestCase
from rest_framework.views import status

from .data import login_info, login_info2, comment, comment2
from authors.apps.authentication.models import User


class CommentArticleTest(BaseTestCase):

    def setUp(self):
        response = self.log_in_user(login_info)
        self.token = response.data['token']
        response2 = self.log_in_user(login_info2)
        self.token2 = response2.data['token']
        slug = 'code'
        id = 2
        self.url = reverse("comments:comment", args=[slug])
        self.url2 = reverse("comments:specific_comment", args=[slug, id])
        self.url3 = reverse("comments:comment_thread", args=[slug, id])

    def test_get_all_comments_for_a_specific_article(self):
        """Tests users can get all comments on an article"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_comment_for_a_specific_article(self):
        """Tests users can get a single comment"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment']['body'],
                         "Your welcome")

    def test_create_comment_for_article(self):
        """Tests users can comment on an article"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url, comment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         'Comment Successfully added')

    def test_update_comment_for_article(self):
        """Tests users can update a comment"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(self.url2, comment2)
        self.assertEqual(response.data['message'],
                         'Comment successfully updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_for_an_article(self):
        """Tests users can delete a comment"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(self.url2)
        self.assertEqual(response.data['message'],
                         'Comment successfully deleted')

    def test_comment_on_comment(self):
        """Tests creating a thread of successive comments"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url3, comment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         "Comment Thread Successfully added")

    def test_get_comments_of_comment(self):
        """Tests getting an entire thread of comments"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_on_non_existant_article(self):
        """Tests commenting on articles that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(
            reverse("comments:comment", args=['blah']), comment)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existant_article(self):
        """Tests getting articles that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse("comments:comment", args=['blah']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_of_non_exitant_article(self):
        """Tests getting comments of articles that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(
            reverse("comments:specific_comment", args=['blah', 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existant_comment_of_article(self):
        """Tests getting comments that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(
            reverse("comments:specific_comment", args=['code', 0]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment_for_non_existant_article(self):
        """Tests updating comments for articles that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(
            reverse("comments:specific_comment", args=['blah', 1]), comment2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existant_comment_for_article(self):
        """Tests updating comments that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(
            reverse("comments:specific_comment", args=['code', 0]), comment2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_for_non_existant_article(self):
        """Tests deleting comments for articles that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(
            reverse("comments:specific_comment", args=['blah', 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existant_comment_for_article(self):
        """Tests deleting comments that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(
            reverse("comments:specific_comment", args=['code', 0]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_thread_on_comment_for_non_existant_article(self):
        """Tests threading on articles that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(
            reverse("comments:comment_thread", args=['blah', 1]), comment)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_thread_on_non_existant_comment_for_article(self):
        """Tests threading on comments that are not created"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(
            reverse("comments:comment_thread", args=['code', 0]), comment)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_unauthored_by_you(self):
        """Tests user cannot delete comment not authored by them"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.delete(self.url2)
        self.assertEqual(response.data['message']['error'],
                         'Unauthorized to delete this comment')

    def test_update_comment_unauthored_by_you(self):
        """Tests user cannot update comment not authored by them"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.put(self.url2, comment2)
        self.assertEqual(response.data['message']['error'],
                         'Unauthorized to update this comment')
