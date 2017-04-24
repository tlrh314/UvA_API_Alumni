from django import template
import re

register = template.Library()

@register.filter
def office(value, arg=3):
    """Turn an office number into a n-digit string, + a possible postifx"""
    try:
        return re.search(r'(?P<office>\d{%d}[a-z]?)$' % arg, value).group('office')
    except AttributeError:
        return ''
