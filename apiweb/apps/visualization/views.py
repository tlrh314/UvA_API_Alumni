from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView


def tree(request):
    return render(request, "visualization/tree.html")
