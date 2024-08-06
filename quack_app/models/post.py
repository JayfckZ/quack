from django import forms
from django.db import models
from .user import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.parent.count()

    def __str__(self):
        return f"{self.user.handle} postou {self.content}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.handle} comentou {self.content} em {self.post}"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
