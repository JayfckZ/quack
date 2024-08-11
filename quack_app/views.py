from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from quack_app.forms import UserRegistrationForm, UserLoginForm
from .models import User, Post, PostForm, Comment, CommentForm


# Create your views here.
def register_login(request):
    if request.method == "POST":
        if "register" in request.POST:
            name = request.POST.get("name")
            handle = request.POST.get("handle")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            
            # Verifica se as senhas são iguais
            if password1 != password2:
                messages.error(request, "As senhas não coincidem.")
                return render(request, "register_login.html")

        # Cria o novo usuário
            try:
                user = User.objects.create_user(name=name, handle=handle, email=email, password=password1)
                user.save()

                # Faz o login automático do usuário
                login(request, user)
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao criar o usuário: {e}")
                return render(request, "register_login.html")
        elif "login" in request.POST:
            handle = request.POST.get("handle")
            password = request.POST.get("password")
            user = authenticate(request, handle=handle, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        return render(request, "register_login.html")


def logout_view(request):
    logout(request)
    return redirect("register_login")


@login_required
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
        request,
        "home.html",
        {"quacks": quacks, "network_quacks": network_quacks, "form": form},
    )


@login_required
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


@login_required
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


@login_required
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


@login_required
def search_users(request):
    query = request.GET.get("q", "")
    if query:
        users = User.objects.filter(
            Q(handle__icontains=query) | Q(name__icontains=query)
        )[:10]
        results = []
        for user in users:
            results.append(
                {
                    "name": user.name,
                    "handle": user.handle,
                    "profile_pic_url": user.profile_pic.url,
                    "is_staff": user.is_staff,
                }
            )

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
