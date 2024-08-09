from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<str:handle>/", views.profile, name="profile"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
]
