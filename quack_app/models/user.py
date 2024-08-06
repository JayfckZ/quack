from django.db import models
from django.contrib.auth.models import AbstractUser
from quack_app.validators import validate_handle


class User(AbstractUser):
    name = models.CharField(max_length=50)
    handle = models.CharField(max_length=30, unique=True, validators=[validate_handle])
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=255, blank=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/", default="profile_pics/profile_default.jpg"
    )
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="user_following"
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="user_followers"
    )

    USERNAME_FIELD = "handle"
    REQUIRED_FIELDS = ["name", "email"]

    def follow(self, user):
        """Seguir um usuário"""
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        """Deixar de seguir um usuário"""
        if user != self:
            self.following.remove(user)

    def is_following(self, user):
        """Verifica se está seguindo um usuário"""
        return self.following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        """Verifica se é seguido pelo usuário"""
        return self.followers.filter(pk=user.pk).exists()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.handle
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} @{self.handle}"
