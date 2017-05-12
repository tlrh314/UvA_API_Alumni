from __future__ import unicode_literals, absolute_import, division

import os.path

from django import template
from django.db.models import Q
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Alumnus, Degree


register = template.Library()


def alumnus_list(request):
    alumni = Alumnus.objects.all()

    # Get filters
    defence_year = request.GET.getlist('year', None)
    degree_type = request.GET.getlist('type', None)
    position = request.GET.getlist('position', None)

    if position:
        multifilter = Q()
        for position in position:
            pass
            # TODO: implement filter for position, e.g. postdoc, staff, nova, etc
            # multifilter = multifilter | Q(degrees__type=degree)

        # alumni = alumni.filter(multifilter).distinct()

    if defence_year:
        multifilter = Q()
        for year in defence_year:

            end_year = str(int(year) + 10)
            if year == "1900":
                end_year = str(int(year) + 50)
            date_range=[year+"-01-01",end_year+"-01-01"]
            multifilter = multifilter | Q(degrees__date_of_defence__range=date_range)
            multifilter = multifilter | Q(degrees__date_stop__range=date_range)

        alumni = alumni.filter(multifilter).distinct()

    if degree_type:
        multifilter = Q()
        for degree in degree_type:
            multifilter = multifilter | Q(degrees__type=degree)

        alumni = alumni.filter(multifilter).distinct()


    alumni_per_page = request.GET.get('limit', 15)

    try:
        alumni_per_page = int(alumni_per_page)
    except ValueError as ScriptKiddyHackings :
        if "invalid literal for int() with base 10:" in str(ScriptKiddyHackings):
            msg = "Error: '{0}' is not a valid limit, please use a number.".format(alumni_per_page)
            messages.error(request, msg)
            alumni_per_page = 15
        else:
            raise Http404

    if alumni_per_page < 15:
        msg = "Error: '{0}' is not a valid limit, please use a number above 15.".format(alumni_per_page)
        alumni_per_page = 15
        messages.error(request, msg)
    if alumni_per_page > 200:
        msg = "Error: '{0}' is not a valid limit, please use a number below 200.".format(alumni_per_page)
        messages.error(request, msg)
        alumni_per_page = 200

    paginator = Paginator(alumni, alumni_per_page)
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except ValueError as ScriptKiddyHackings :
        if "invalid literal for int() with base 10:" in str(ScriptKiddyHackings):
            msg = "Error: '{0}' is not a valid pagenumber, please use a number.".format(page)
            messages.error(request, msg)
            page = 1
        else:
            raise Http404

    try:
        alumni = paginator.page(page)
    except PageNotAnInteger:
        msg = "Error: '{0}' is not a valid pagenumber.".format(page)
        messages.error(request, msg)
        alumni = paginator.page(1)
    except EmptyPage:
        msg = "Error: '{0}' is not a valid pagenumber.".format(page)
        messages.error(request, msg)
        alumni = paginator.page(paginator.num_pages)


    return render(request, "alumni/alumnus_list.html", {"alumni": alumni,
        "alumni_per_page": int(alumni_per_page)})


def alumnus_detail(request, slug):
    alumnus = get_object_or_404(Alumnus, slug=slug)

    return render(request, "alumni/alumnus_detail.html", {"alumnus": alumnus})


def thesis_list(request):
    # TODO: implement filtering on MSc / PhD
    theses = Degree.objects.filter(type="phd")
    theses = theses.order_by("-date_of_defence")
    theses_counter = range(len(theses), 0, -1)

    theses_per_page = request.GET.get('limit', 15)
    try:
        theses_per_page = int(theses_per_page)
    except ValueError as ScriptKiddyHackings :
        if "invalid literal for int() with base 10:" in str(ScriptKiddyHackings):
            msg = "Error: '{0}' is not a valid limit, please use a number.".format(theses_per_page)
            messages.error(request, msg)
            theses_per_page = 15
        else:
            raise Http404

    if theses_per_page < 15:
        msg = "Error: '{0}' is not a valid limit, please use a number above 15.".format(theses_per_page)
        messages.error(request, msg)
        theses_per_page = 15
    if theses_per_page > 200:
        msg = "Error: '{0}' is not a valid limit, please use a number below 200.".format(theses_per_page)
        messages.error(request, msg)
        theses_per_page = 200

    paginator = Paginator(theses, theses_per_page)
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except ValueError as ScriptKiddyHackings :
        if "invalid literal for int() with base 10:" in str(ScriptKiddyHackings):
            msg = "Error: '{0}' is not a valid pagenumber, please use a number.".format(page)
            messages.error(request, msg)
            page = 1
        else:
            raise Http404

    try:
        phd_theses = paginator.page(page)
    except PageNotAnInteger:
        msg = "Error: '{0}' is not a valid pagenumber.".format(page)
        messages.error(request, msg)
        page = 1
        phd_theses = paginator.page(page)
    except EmptyPage:
        msg = "Error: '{0}' is not a valid pagenumber.".format(page)
        messages.error(request, msg)
        page = paginator.num_pages
        phd_theses = paginator.page(page)


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

    # TODO: de 404 werkt niet bij missende pdf
    theses_list_start = (page-1)*theses_per_page
    theses_list_stop = page*theses_per_page
    theses_counter = theses_counter[theses_list_start: theses_list_stop]
    theses_title_pdf_counter = zip(phd_theses, has_title, has_pdf, theses_counter)

    # TODO: very ugly way of returning things. Fix it to avoid returning theses twice
    return render(request, "alumni/thesis_list.html", {
        "theses": phd_theses, "theses_per_page": theses_per_page,
        "theses_title_pdf_counter": theses_title_pdf_counter })


def thesis_detail(request, thesis_slug):
    thesis = get_object_or_404(Degree, thesis_slug=thesis_slug)

    return render(request, "alumni/thesis_detail.html", {"thesis": thesis})



def thesis_has_no_pdf(request):
    return render(request, "alumni/thesis_not_found.html")
