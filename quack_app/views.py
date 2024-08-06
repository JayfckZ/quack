from django.shortcuts import render, get_object_or_404
from .models import User, Post


# Create your views here.
def home(request):
    quacks = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"quacks": quacks})

def profile(request, handle):
    user = get_object_or_404(User, handle=handle)
    quacks = Post.objects.filter(user=user)
    return render(request, "profile.html", {"user": user, "quacks": quacks})
