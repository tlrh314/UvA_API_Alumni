from django import template

from ...alumni.models import Alumnus

register = template.Library()


@register.filter
def author_name(post):
    alumnus = Alumnus.objects.filter(user=post.author)
    if alumnus:
        return alumnus.full_name
    else:
        return post.author
