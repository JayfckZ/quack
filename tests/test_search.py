from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quack_app.models import Post
from quack_app.factories import UserFactory, PostFactory

User = get_user_model()

class FollowUserTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.client.login(username=self.user1.username, password='defaultpassword')

    def test_follow_user(self):
        response = self.client.post(reverse('follow_user', args=[self.user2.handle]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user1.is_following(self.user2))

    def test_unfollow_user(self):
        self.user1.follow(self.user2)
        response = self.client.post(reverse('unfollow_user', args=[self.user2.handle]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user1.is_following(self.user2))
