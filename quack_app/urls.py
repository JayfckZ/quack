from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<str:handle>/", views.profile, name="profile"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("follow/<str:handle>/", views.follow_user, name="follow_user"),
    path("unfollow/<str:handle>/", views.unfollow_user, name="unfollow_user"),
    path("search-users/", views.search_users, name="search_users"),
    path("register-login/", views.register_login, name="register_login"),
    path("logout/", views.logout_view, name="logout"),
    path('edit/', views.edit, name='edit'),
]
