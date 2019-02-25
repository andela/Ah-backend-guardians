from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.utils.serializer_helpers import OrderedDict
from rest_framework.test import APITestCase, APIClient
from authors.apps.authentication.tests.base import BaseTestCase

from authors.apps.authentication.tests.data import login_info
from authors.apps.articles.tests.data import login_info2
from authors.apps.profiles.models import ReadingStat
from ..models import Article, Bookmark
from .data import article_body
from authors.apps.authentication.models import User
from rest_framework.test import (
    APITestCase,
    APIClient
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
        self.rate = {

            "score": 5
        }
        self.rate_high_score = {

            "score": 8
        }

        self.url = reverse('article:create_article')
        self.url1 = reverse('article:create_article')

    def get_user_token(self):
        request = self.log_in_user(login_info)
        return request.data['token']

    def get_second_user_token(self):
        request = self.log_in_user(login_info2)
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

    def test_rate_article_you_created(self):
        """
        Test to check whether you can rate an article you created
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        rate_url = reverse('article:ratings_list', args=[slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.put(
            rate_url, data=self.rate, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(response.data['error'],
                         'You cannot rate an article you created')

    def test_successfully_rate_article(self):
        """
        Test to check whether you can rate an article successfully
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        rate_url = reverse('article:ratings_list', args=[slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_second_user_token())
        response2 = self.client.put(
            rate_url, data=self.rate, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['score'], 5)

    def test_rating_an_article_with_too_high_a_score(self):
        """
        Test rating an article with a score that is too high
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        rate_url = reverse('article:ratings_list', args=[slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_second_user_token())
        response2 = self.client.put(
            rate_url, data=self.rate_high_score, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_article_does_not_exist(self):
        """
        Test trying to rate an article that does not exist
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        rate_url = self.url+slug+'yy/rating/'
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_second_user_token())
        response2 = self.client.put(
            rate_url, data=self.rate_high_score, format='json')
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.data['detail'],
                         'Not found.')

    def test_like_article_doesnot_exist(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = "vivian-cohort"
        like_url = reverse("article:like_article", args=[slug])
        get_response = self.client.put(like_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_article_that_exists(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        like_url = reverse("article:like_article", args=[slug])
        get_response = self.client.put(like_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['message'], 'liked')

    def test_like_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        like_url = reverse("article:like_article", args=[slug])
        like_response = self.client.put(like_url, format='json')
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['message'], 'liked')

    def test_like_article_you_disliked(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        dislike_url = reverse("article:dislike_article", args=[slug])
        dislike_response = self.client.put(dislike_url, format='json')
        like_url = reverse("article:like_article", args=[slug])
        like_response = self.client.put(like_url, format='json')
        self.assertEqual(dislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dislike_response.data['message'], 'disliked')
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['message'], 'liked')

    def test_unlike_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        like_url = reverse("article:like_article", args=[slug])
        like_response = self.client.put(like_url, format='json')
        unlike_response = self.client.put(like_url, format='json')
        unlike_like_response = self.client.put(like_url, format='json')
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['message'], 'liked')
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data['message'], 'unliked')
        self.assertEqual(unlike_like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_like_response.data['message'], 'liked')

    def test_dislike_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        dislike_url = reverse("article:dislike_article", args=[slug])
        dislike_response = self.client.put(dislike_url, format='json')
        self.assertEqual(dislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dislike_response.data['message'], 'disliked')

    def test_dislike_article_you_liked(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        like_url = reverse("article:like_article", args=[slug])
        like_response = self.client.put(like_url, format='json')
        dislike_url = reverse("article:dislike_article", args=[slug])
        dislike_response = self.client.put(dislike_url, format='json')
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['message'], 'liked')
        self.assertEqual(dislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dislike_response.data['message'], 'disliked')

    def test_undislike_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data.get('slug')
        dislike_url = reverse("article:dislike_article", args=[slug])
        dislike_response = self.client.put(dislike_url, format='json')
        undislike_response = self.client.put(dislike_url, format='json')
        undislike_dislike_response = self.client.put(
            dislike_url, format='json')
        self.assertEqual(dislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dislike_response.data['message'], 'disliked')
        self.assertEqual(undislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(undislike_response.data['message'], 'undisliked')
        self.assertEqual(
            undislike_dislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            undislike_dislike_response.data['message'], 'disliked')

    def test_get_like_article_that_doesnot_exist(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        dislike_url = reverse("article:dislike_article", args=[slug])
        self.client.put(dislike_url, format='json')
        get_like_url = reverse("article:get_article_like", args=[slug])
        get_like_response = self.client.get(get_like_url, format='json')
        self.assertEqual(get_like_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            get_like_response.data, {'article_like': False})

    def test_get_like_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        like_url = reverse("article:like_article", args=[slug])
        self.client.put(like_url, format='json')
        get_like_url = reverse("article:get_article_like", args=[slug])
        get_like_response = self.client.get(get_like_url, format='json')
        self.assertEqual(get_like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_like_response.data, {'article_like': True})

    def test_get_dislike_article_that_doesnot_exist(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        like_url = reverse("article:like_article", args=[slug])
        self.client.put(like_url, format='json')
        get_dislike_url = reverse("article:get_article_dislike", args=[slug])
        get_dislike_response = self.client.get(get_dislike_url, format='json')
        self.assertEqual(get_dislike_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(
            get_dislike_response.data, {'article_dislike': False})

    def test_get_dislike_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        dislike_url = reverse("article:dislike_article", args=[slug])
        self.client.put(dislike_url, format='json')
        get_dislike_url = reverse("article:get_article_dislike", args=[slug])
        get_dislike_response = self.client.get(get_dislike_url, format='json')
        self.assertEqual(get_dislike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_dislike_response.data, {'article_dislike': True})

    def test_try_and_fail_to_rate_an_article_again(self):
        """
        Test to check whether you can rate an article a second
        time
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        rate_url = reverse('article:ratings_list', args=[slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_second_user_token())
        response2 = self.client.put(
            rate_url, data=self.rate, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_second_user_token())
        response3 = self.client.put(
            rate_url, data=self.rate, format='json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.data['error'],
                         'You already rated this article')

    def test_get_facebook_link(self):
        """Test if the user can get facebook link"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        fb_response = self.client.get(
            reverse("article:detail", args=[slug]),  format='json')
        self.assertEqual(fb_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            fb_response.data['social_links']['facebook'],
            'https://www.facebook.com/sharer/sharer.php?'
            'u=http%3A//testserver/api/articles/my-best-day-in-2018/')

    def test_get_twitter_link(self):
        """Test if the user can get twitter link"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        tw_response = self.client.get(
            reverse("article:detail", args=[slug]),  format='json')
        self.assertEqual(tw_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            tw_response.data['social_links']['twitter'],
            "https://twitter.com/home?status=http%3A//"
            "testserver/api/articles/my-best-day-in-2018/")

    def test_email_article_link(self):
        """Test if the user can send email link"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url1, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.get(
            reverse("article:detail", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_200_OK)

    def test_read_article(self):
        """Tests that user is added to database after reading an article"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.get(
            self.url + 'coding/', format='json')
        user = User.objects.get(email="f.faraqhan91234@gmail.com")
        article = Article.objects.get(slug='coding')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ReadingStat.objects.all().filter(
            user=user.username, articles=article.slug))

    def test_get_my_articles(self):
        """Tests that a user can get only articles they authored"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.get(
            self.url + 'my_articles/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_bookmark_article_object_created(self):
        """Test if the bookmark object created"""
        user = User.objects.create_user(
            username='moses', email='moses@gmail.com',
            password='Kamira123')
        reader = User.objects.create_user(
            username='fahad', email='fahad@gmail.com',
            password='Kamira123')
        user.is_verified = True
        user = User.objects.filter(email='moses@gmail.com').first()
        author = user
        article = Article.objects.create(
            title='article title', author=author)
        bookmark = Bookmark.objects.create(
            article=article, reader=reader)
        self.assertIsInstance(bookmark, Bookmark)

    def test_bookmark_article(self):
        """Test if the user can bookmark an article"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(em_response.data.get(
            'title'), self.article.get('title'))

    def test_cant_bookmark_article_that_doesnt_exist(self):
        """Test if the user can bookmark an article"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = 'twenty'
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(em_response.data.get(
            'error'), 'Article  your trying to bookmark does not exist')

    def test_article_already_bookmark(self):
        """Test if the user cannot bookmark an article again"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_201_CREATED)
        bookmark_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(bookmark_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(bookmark_response.data['message'],
                         f"You have unbookmarked this "
                         f"article called {self.article['title']}")

    def test_return_all_your_bookmarks(self):
        """Test if the user view all bookmarks"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_201_CREATED)
        bookmark_response = self.client.get(
            reverse("article:bookmarks"), format='json')
        self.assertTrue(bookmark_response.data)
        self.assertEqual(bookmark_response.status_code,
                         status.HTTP_200_OK)

    def test_delete_bookmark(self):
        """Test if the user can delete a bookmark"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_201_CREATED)
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]), format='json')
        self.assertEqual(em_response.status_code, status.HTTP_200_OK)
        self.assertEqual(em_response.data.get('message'),
                         f"You have unbookmarked this "
                         f"article called {self.article['title']}")

    def test_get_one_bookmark(self):
        """Test if the user can delete a bookmark"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_201_CREATED)
        bookmark = em_response.data.get('slug')
        em_response = self.client.get(
            reverse("article:bookmark_detail",
                    args=[bookmark]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_200_OK)
        self.assertEqual(em_response.data.get('title'),
                         self.article.get('title'))

    def test_cant_get_bookmark_doesnot_exist(self):
        """Test if the user can't get a bookmark that doesnt exist"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        get_response = self.client.get(
            reverse("article:bookmark_detail", args=['hello']), format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_response.data.get('error'),
                         'Bookmark does not exist')

    def test_cant_get_bookmark_you_didnt_create(self):
        """Test if the user can't get a bookmark he didnt create"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(
            self.url, data=self.article, format='json')
        slug = response.data.get('slug')
        em_response = self.client.put(
            reverse("article:create_bookmark", args=[slug]),  format='json')
        self.assertEqual(em_response.status_code, status.HTTP_201_CREATED)
        bookmark = em_response.data.get('slug')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_second_user_token())
        lf_response = self.client.get(
            reverse("article:bookmark_detail", args=[bookmark]), format='json')
        self.assertEqual(lf_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(lf_response.data.get('error'),
                         'You do not have permission to perform this action.')
