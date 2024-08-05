from django.db import models
from django.contrib.auth.models import AbstractUser
from quack_app.validators import validate_handle

class User(AbstractUser):
    name = models.CharField(max_length=50)
    handle = models.CharField(
        max_length=30, 
        unique=True, 
        validators=[validate_handle]
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'handle'
    REQUIRED_FIELDS = ['name', 'email']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.handle
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} @{self.handle}"
