from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quack_app.models import Post
from quack_app.factories import UserFactory, PostFactory

User = get_user_model()

class LikePostTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.client.login(username=self.user1.username, password='defaultpassword')
        
        self.post = PostFactory(user=self.user2)

    def test_like_post(self):
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"liked": True, "total_likes": 1})
        self.assertTrue(self.post.likes.filter(id=self.user1.id).exists())

    def test_unlike_post(self):
        self.post.likes.add(self.user1)
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"liked": False, "total_likes": 0})
        self.assertFalse(self.post.likes.filter(id=self.user1.id).exists())
