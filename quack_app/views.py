from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User, Post, CommentForm, Comment


# Create your views here.
def home(request):
    quacks = Post.objects.all().order_by("-created_at")
    followed_users = request.user.user_following.all()
    network_quacks = Post.objects.filter(user__in=followed_users).order_by("-created_at")
    return render(request, "home.html", {"quacks": quacks, "network_quacks": network_quacks})


def profile(request, handle):
    user = get_object_or_404(User, handle=handle)
    quacks = Post.objects.filter(user=user).order_by("-created_at")
    comments = Comment.objects.filter(user=user).order_by("-created_at")
    is_following = request.user.is_authenticated and request.user.is_following(user)
    is_followed = request.user.is_authenticated and request.user.is_followed_by(user)
    return render(request, "profile.html", {"user": user, "quacks": quacks, "comments": comments, "is_following": is_following, "is_followed": is_followed})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by("-created_at")
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect("post_detail", post_id=post_id)

    return render(
        request, "post_detail.html", {"post": post, "comments": comments, "form": form}
    )


def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({"liked": liked, "total_likes": post.total_likes()})
    return JsonResponse({'error': 'Not authenticated'}, status=401)


@login_required
def follow_user(request, handle):
    user_to_follow = get_object_or_404(User, handle=handle)
    request.user.follow(user_to_follow)
    return redirect('profile', handle=handle)

@login_required
def unfollow_user(request, handle):
    user_to_unfollow = get_object_or_404(User, handle=handle)
    print(user_to_unfollow)
    request.user.unfollow(user_to_unfollow)
    return redirect('profile', handle=handle)