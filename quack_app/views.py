from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import User, Post, CommentForm, Comment


# Create your views here.
def home(request):
    quacks = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"quacks": quacks})


def profile(request, handle):
    user = get_object_or_404(User, handle=handle)
    quacks = Post.objects.filter(user=user).order_by("-created_at")
    comments = Comment.objects.filter(user=user).order_by("-created_at")
    return render(request, "profile.html", {"user": user, "quacks": quacks, "comments": comments})


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
