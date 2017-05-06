from django import template
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Post
# from models import Category

register = template.Library()

def index(request, category=None):
    posts = Post.objects.filter(is_published=True)

    return render(request, "interviews/index.html", {"posts": posts })


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, "interviews/details.html", {"post": post })
