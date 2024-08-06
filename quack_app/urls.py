from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<str:handle>/", views.profile, name="profile"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
]
