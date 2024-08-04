from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50)
    handle = models.CharField(max_length=30, unique=True)
    bio = models.TextField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} @{self.handle}"
