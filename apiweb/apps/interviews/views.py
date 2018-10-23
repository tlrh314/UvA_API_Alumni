from django import template
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post
# from models import Category

register = template.Library()


@login_required
def index(request, category=None):
    posts = Post.objects.filter(is_published=True)

    return render(request, "interviews/index.html", {"posts": posts })


@login_required
def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, "interviews/details.html", {"post": post })
