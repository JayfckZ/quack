from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, Post, PostForm, Comment, CommentForm


# Create your views here.
def home(request):
    quacks = Post.objects.all().order_by("-created_at")
    followed_users = request.user.user_following.all()
    network_quacks = Post.objects.filter(user__in=followed_users).order_by(
        "-created_at"
    )
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect("home")

    return render(
        request, "home.html", {"quacks": quacks, "network_quacks": network_quacks, "form": form}
    )


def profile(request, handle):
    user = get_object_or_404(User, handle=handle)
    quacks = Post.objects.filter(user=user).order_by("-created_at")
    comments = Comment.objects.filter(user=user).order_by("-created_at")
    liked = Post.objects.filter(likes=user).order_by("-created_at")
    is_following = request.user.is_authenticated and request.user.is_following(user)
    is_followed = request.user.is_authenticated and request.user.is_followed_by(user)
    return render(
        request,
        "profile.html",
        {
            "user": user,
            "quacks": quacks,
            "comments": comments,
            "is_following": is_following,
            "is_followed": is_followed,
            "liked": liked,
        },
    )


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
    return JsonResponse({"error": "Not authenticated"}, status=401)


def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(handle__icontains=query) | Q(name__icontains=query)
        )[:10]
        results = []
        for user in users:
            results.append({
                'name': user.name,
                'handle': user.handle,
                'profile_pic_url': user.profile_pic.url,
                'is_staff': user.is_staff
            })

    else:
        results = []
    return JsonResponse(results, safe=False)


@login_required
def follow_user(request, handle):
    user_to_follow = get_object_or_404(User, handle=handle)
    request.user.follow(user_to_follow)
    return redirect("profile", handle=handle)


@login_required
def unfollow_user(request, handle):
    user_to_unfollow = get_object_or_404(User, handle=handle)
    request.user.unfollow(user_to_unfollow)
    return redirect("profile", handle=handle)
