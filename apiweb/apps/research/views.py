from __future__ import unicode_literals, absolute_import, division

import os.path

from django import template
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..research.models import Thesis


register = template.Library()


def thesis_list(request):
    theses = Thesis.objects.all()

    # Get filters
    defence_year = request.GET.getlist("year", None)
    thesis_types = request.GET.getlist("type", None)
    sort_on = request.GET.getlist("sort", None)

    # Apply filters
    if thesis_types:
        multifilter = Q()
        for thesis_type in thesis_types:
            multifilter = multifilter | Q(type=thesis_type)

        theses = theses.filter(multifilter).distinct()

    if defence_year:
        multifilter = Q()
        for year in defence_year:

            try:
                end_year = str(int(year) + 10)
            except ValueError as e:
                if "invalid literal for int() with base 10" in str(e):
                    raise Http404

            if year == "1900":
                end_year = str(int(year) + 50)
            date_range=[year+"-01-01",end_year+"-01-01"]
            multifilter = multifilter | Q(date_of_defence__range=date_range)
            multifilter = multifilter | Q(date_stop__range=date_range)

        theses = theses.filter(multifilter).distinct()

    # Sort the list
    if sort_on:
        if sort_on[0] == "author_az":
            theses = theses.order_by("alumnus__last_name")
        if sort_on[0] == "author_za":
            theses = theses.order_by("-alumnus__last_name")

        if sort_on[0] == "title_az":
            theses = theses.order_by("title")
        if sort_on[0] == "title_za":
            theses = theses.order_by("-title")

        # Caution: sorting on degree/position implies filtering also
        if sort_on[0] == "msc_lh":
            theses = theses.filter(type__iexact="msc").distinct().order_by("date_of_defence")
        if sort_on[0] == "msc_hl":
            theses = theses.filter(type__iexact="msc").distinct().order_by("-date_of_defence")

        if sort_on[0] == "phd_lh":
            theses = theses.filter(type__iexact="phd").distinct().order_by("date_of_defence")
        if sort_on[0] == "phd_hl":
            theses = theses.filter(type__iexact="phd").distinct().order_by("-date_of_defence")

        # Year filter for date of defence which includes both MSc and PhD
        if sort_on[0] == "year_lh":
            theses = theses.order_by("date_of_defence")
        if sort_on[0] == "year_hl":
            theses = theses.order_by("-date_of_defence")
    else:
        theses = theses.order_by("-date_of_defence")

    # Paginate the list
    theses_per_page = request.GET.get("limit", 15)
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
        theses = paginator.page(page)
    except PageNotAnInteger:
        msg = "Error: '{0}' is not a valid pagenumber.".format(page)
        messages.error(request, msg)
        page = 1
        theses = paginator.page(page)
    except EmptyPage:
        msg = "Error: '{0}' is not a valid pagenumber.".format(page)
        messages.error(request, msg)
        page = paginator.num_pages
        theses = paginator.page(page)

    return render(request, "research/thesis_list.html", {
        "theses": theses, "theses_per_page": theses_per_page })

def thesis_detail(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug)
    return render(request, "research/thesis_detail.html", {"thesis": thesis})

def thesis_has_no_pdf(request):
    return render(request, "research/thesis_not_found.html")
