from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quack_app.models import Post
from quack_app.factories import UserFactory, PostFactory

User = get_user_model()

class HomeViewTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.client.login(username=self.user1.username, password='defaultpassword')
        
        self.post1 = PostFactory(user=self.user1)
        self.post2 = PostFactory(user=self.user2)

    def test_home_view_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_shows_posts(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.post1.content)

    def test_home_view_shows_followed_users_posts(self):
        self.user1.follow(self.user2)
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.post2.content)
