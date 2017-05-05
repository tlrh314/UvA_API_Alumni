from __future__ import unicode_literals, absolute_import, division

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def paginate(page, arg="3,2"):
    """  Provide a HTML rendered pagination section, with leading,
    trailing and surrounding page numbers

    First part of the argument is the number of surrounding page numbers,
    the second part the number of leading and trailing page numbers
    at the start and end.

    Other examples at:
    http://code.djangoproject.com/wiki/PaginatorTag
    http://blog.localkinegrinds.com/2007/09/06/digg-style-pagination-in-django/

    """

    args = [int(val) for val in arg.split(',')]
    if len(args) > 0:
        surrounding = args[0]
        leading = trailing = 2
    if len(args) > 1:
        leading = trailing = args[1]
    paginator = page.paginator
    if (paginator.num_pages == 1 or 0 in [surrounding, leading, trailing]):
        return ""
    current = page.number
    firstpage, lastpage = 1, paginator.num_pages
    start = set(range(firstpage, leading+1))
    end = set(range(lastpage+1-trailing, lastpage+1))
    surround = set(range(max(1, current-surrounding),
                         min(lastpage+1, current+surrounding+1)))
    ellipses = True, True
    if start.intersection(surround) or max(start)+1 == min(surround):
        start = start.union(surround)
        surround = set()
        ellipses = False, True
    elif end.intersection(surround) or min(end)-1 == max(surround):
        end = end.union(surround)
        surround = set()
        ellipses = True, False
    if start.intersection(end) or max(start)+1 == min(end):
        start = start.union(end)
        end = set()
        surround = ()
        ellipses = False, False
    pagenumbers = []
    if current > 1:
        pagenumbers.append('<a href="?page={}">previous</a>'.format(current-1))
    for num in sorted(start):
        if num == current:
            pagenumbers.append('{}'.format(num))
        else:
            pagenumbers.append('<a href="?page={}">{}</a>'.format(num, num))
    if ellipses[0]:
        pagenumbers.append('...')
    for num in sorted(surround):
        if num == current:
            pagenumbers.append('{}'.format(num))
        else:
            pagenumbers.append('<a href="?page={}">{}</a>'.format(num, num))
    if ellipses[1]:
        pagenumbers.append('...')
    for num in sorted(end):
        if num == current:
            pagenumbers.append('{}'.format(num))
        else:
            pagenumbers.append('<a href="?page={}">{}</a>'.format(num, num))
    if current < lastpage:
        pagenumbers.append('<a href="?page={}">next</a>'.format(current+1))
    return mark_safe("|".join(pagenumbers))
