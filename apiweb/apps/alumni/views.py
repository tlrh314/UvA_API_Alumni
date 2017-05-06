from __future__ import unicode_literals, absolute_import, division

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView

from .models import Alumnus, Degree

def alumnus_list(request):
    alumni = Alumnus.objects.all()

    return render(request, "alumni/alumnus_list.html", {"alumni": alumni})

def alumnus_detail(request, slug):
    alumnus = get_object_or_404(Alumnus, slug=slug)

    return render(request, "alumni/alumnus_detail.html", {"alumnus": alumnus})


def thesis_list(request):
    theses = Degree.objects.filter(type="phd")

    return render(request, "alumni/thesis_list.html", {"theses": theses })

def thesis_detail(request, thesis_slug):
    thesis = get_object_or_404(Degree, thesis_slug=thesis_slug)

    return render(request, "alumni/thesis_detail.html", {"thesis": thesis})
