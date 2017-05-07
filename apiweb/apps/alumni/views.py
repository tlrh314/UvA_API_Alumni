from __future__ import unicode_literals, absolute_import, division

import os.path

from django import template
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Alumnus, Degree

register = template.Library()

def alumnus_list(request):
    alumni = Alumnus.objects.all()

    # Get filters
    gender = request.GET.getlist('gender', None)
    defence_year = request.GET.getlist('year', None)
    degree_type = request.GET.getlist('type', None)

    # Apply filters
    if gender:
        alumni = alumni.filter(gender=gender[0])

    if defence_year:
        multifilter = Q()
        for year in defence_year:

            end_year = str(int(year) + 10)
            date_range=[year+"-01-01",end_year+"-01-01"]
            multifilter = multifilter | Q(degrees__date_of_defence__range=date_range)
            multifilter = multifilter | Q(degrees__date_stop__range=date_range)

        alumni = alumni.filter(multifilter).distinct()

    if degree_type:
        multifilter = Q()
        for degree in degree_type:
            multifilter = multifilter | Q(degrees__type=degree)

        alumni = alumni.filter(multifilter).distinct()

    return render(request, "alumni/alumnus_list.html", {"alumni": alumni})

def alumnus_detail(request, slug):
    alumnus = get_object_or_404(Alumnus, slug=slug)

    return render(request, "alumni/alumnus_detail.html", {"alumnus": alumnus})

def thesis_list(request):
    # TODO: implement filtering on MSc / PhD, selecting theses_per_page
    theses = Degree.objects.filter(type="phd")
    theses = theses.order_by("-date_of_defence")

    theses_per_page = request.GET.get('limit', '15')

    # Validate input (protection agains hacking..)
    if not theses_per_page.isdigit():
        theses_per_page = 15

    paginator = Paginator(theses, theses_per_page)
    page = request.GET.get('page', 1)

    try:
        phd_theses = paginator.page(page)
    except PageNotAnInteger:
        phd_theses = paginator.page(1)
    except EmptyPage:
        phd_theses = paginator.page(paginator.num_pages)

    has_title = dict()
    has_pdf = dict()
    for thesis in phd_theses:
        if thesis.thesis_title:
            has_title[thesis.thesis_slug] = True
        else:
            has_title[thesis.thesis_slug] = False

        if os.path.exists(settings.STATIC_ROOT+"/alumni/theses/phd/"+thesis.thesis_slug):
            has_pdf[thesis.thesis_slug] = True
        else:
            has_pdf[thesis.thesis_slug] = False

    theses_title_pdf = zip(phd_theses, has_title, has_pdf)

    # TODO: very ugly way of returning things. Fix it to avoid returning theses double
    return render(request, "alumni/thesis_list.html", {
        "theses": phd_theses,
        "theses_title_pdf": theses_title_pdf })

def thesis_detail(request, thesis_slug):
    thesis = get_object_or_404(Degree, thesis_slug=thesis_slug)

    return render(request, "alumni/thesis_detail.html", {"thesis": thesis})
