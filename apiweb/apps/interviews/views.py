from django.shortcuts import render
from django import template
from django.http import Http404
from django.shortcuts import get_object_or_404

from models import Post
# from models import Category

register = template.Library()

def blog(request, category=None):
    posts = Post.objects.filter(is_published=True)

    # categories = Category.objects.all()
    # if category:
    #     posts = Post.objects.filter(category=Category.objects.get(type_id=category))
    #     category = get_object_or_404(Category, type_id=category)

    # featured_posts = Post.objects.filter(featured=True)
    # top_stories = Post.objects.filter(top_story=True)

    return render(request, 'blog/blog.html',
        {    # 'categories': categories,
             # 'category': category
            'posts': posts })


def blog_post(request, blog_ID):
    all_categories = Category.objects.all()
    posts = Post.objects.all()

    # categories = Category.objects.all()
    current_post = None

    if blog_ID.endswith('-'):
        blog_ID = blog_ID[:-1]

    # Get the blog post that matches the blog_ID
    for post in posts:
        if post.post_ID() == blog_ID:
            current_post = post

    if current_post is None:
        raise Http404

    return render(request, 'interviews/post.html',
        {    # 'all_categories': all_categories,  'categories': categories,
             'current_post': current_post
        })
