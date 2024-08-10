from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quack_app.models import Post
from quack_app.factories import UserFactory, PostFactory

User = get_user_model()

class SearchUsersTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory(name="John Doe", handle="johndoe")
        self.user2 = UserFactory(name="Jane Smith", handle="janesmith")
        self.client.login(username=self.user1.username, password='defaultpassword')

    def test_search_users_by_handle(self):
        response = self.client.get(reverse('search_users'), {'q': 'johndoe'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.handle)
        self.assertNotContains(response, self.user2.handle)

    def test_search_users_by_name(self):
        response = self.client.get(reverse('search_users'), {'q': 'Jane'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.name)
        self.assertNotContains(response, self.user1.name)
