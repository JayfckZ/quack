import factory
from django.contrib.auth import get_user_model
from faker import Faker
from .models import Post, Comment

User = get_user_model()
fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    handle = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'user{o.handle}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    class Meta:
        model = User


class PostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    content = factory.Faker('sentence', nb_words=4)

    class Meta:
        model = Post



class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker('sentence', nb_words=4)
