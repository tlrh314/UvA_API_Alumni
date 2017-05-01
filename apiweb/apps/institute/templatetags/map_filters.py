from __future__ import unicode_literals, absolute_import, division

from django import template
import re

register = template.Library()

@register.filter
def office(value, arg=3):
    """Turn an office number into a n-digit string, + a possible postifx"""
    try:
        return re.search(r'(?P<office>\d{{{}}}[a-z]?)$'.format(arg),
                         value).group('office')
    except AttributeError:
        return ''
