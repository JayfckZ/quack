from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quack_app.models import Post
from quack_app.factories import UserFactory, PostFactory, CommentFactory

User = get_user_model()

class ProfileViewTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.client.login(username=self.user1.username, password='defaultpassword')

        self.post1 = PostFactory(user=self.user1)
        self.post2 = PostFactory(user=self.user2)
        self.comment1 = CommentFactory(user=self.user1, post=self.post1)
        self.comment2 = CommentFactory(user=self.user2, post=self.post1)

    def test_profile_view_loads(self):
        response = self.client.get(reverse('profile', args=[self.user1.handle]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_shows_posts(self):
        response = self.client.get(reverse('profile', args=[self.user1.handle]))
        self.assertContains(response, self.post1.content)

    def test_profile_view_shows_comments(self):
        response = self.client.get(reverse('profile', args=[self.user1.handle]))
        self.assertContains(response, self.comment1.content)

    def test_profile_view_follow_status(self):
        response = self.client.get(reverse('profile', args=[self.user2.handle]))
        self.assertContains(response, 'Seguir')

        self.user1.follow(self.user2)
        response = self.client.get(reverse('profile', args=[self.user2.handle]))
        self.assertContains(response, 'Deixar de Seguir')
