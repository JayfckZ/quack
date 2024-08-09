from django.shortcuts import redirect, render, get_object_or_404
from .models import User, Post, CommentForm


# Create your views here.
def home(request):
    quacks = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"quacks": quacks})


def profile(request, handle):
    user = get_object_or_404(User, handle=handle)
    quacks = Post.objects.filter(user=user).order_by("-created_at")
    return render(request, "profile.html", {"user": user, "quacks": quacks})


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
