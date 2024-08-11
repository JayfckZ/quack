from django.db import models
from django.contrib.auth.models import AbstractUser
from quack_app.validators import validate_handle
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, handle, email, name, password=None, **extra_fields):
        if not handle:
            raise ValueError('O campo handle deve ser definido')
        if not email:
            raise ValueError('O campo email deve ser definido')
        
        email = self.normalize_email(email)
        user = self.model(handle=handle, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, handle, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(handle, email, name, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=50)
    handle = models.CharField(max_length=30, unique=True, validators=[validate_handle])
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=255, blank=True)
    profile_pic = ProcessedImageField(
        upload_to='profile_pictures/',
        default="profile_pics/profile_default.jpg",
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60}
    )
    
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="user_following", blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="user_followers", blank=True
    )

    objects = UserManager()
    
    USERNAME_FIELD = "handle"
    REQUIRED_FIELDS = ["name", "email"]

    def clean(self):
        self.handle = self.handle.lower()

    def follow(self, user):
        """Seguir um usuário"""
        if user != self:
            self.user_following.add(user)
            user.user_followers.add(self)

    def unfollow(self, user):
        """Deixar de seguir um usuário"""
        if user != self:
            self.user_following.remove(user)
            user.user_followers.remove(self)

    def is_following(self, user):
        """Verifica se está seguindo um usuário"""
        return self.user_following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        """Verifica se é seguido pelo usuário"""
        return user.user_following.filter(pk=self.pk).exists()

    def total_following(self):
        return self.user_following.count()

    def total_followers(self):
        return self.user_followers.count()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.handle
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} @{self.handle}"
