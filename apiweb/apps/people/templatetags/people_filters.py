from __future__ import unicode_literals, absolute_import, division

from django import template
from django.utils.http import urlquote
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


register = template.Library()


@register.filter
@template.defaultfilters.stringfilter
def ads_url(value, autoescape=None):
    """Returns ADS link based on name or on personal library"""

    # see http://docs.djangoproject.com/en/dev/howto/custom-template-tags/\
    # #filters-and-auto-escaping
    value = conditional_escape(value) if autoescape else value
    link = ''
    if len(value) == 0:
        return mark_safe(link)
    if value.startswith('libname'):
        link = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?library&' + \
               value
    else:
        link = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?' \
               'db_key=AST&db_key=INST&db_key=PHY&author=' + urlquote(value) + \
               '&nr_to_return=2000&start_nr=1'
    return mark_safe(link)
ads_url.needs_autoescape = True
