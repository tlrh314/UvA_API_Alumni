from __future__ import unicode_literals, absolute_import, division

import os.path

from django import template
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Alumnus


register = template.Library()


def alumnus_list(request):
    alumni = Alumnus.objects.all()

    # Get filters
    defence_year = request.GET.getlist("year", None)
    degree_type = request.GET.getlist("type", None)
    positions = request.GET.getlist("positions", None)
    sort_on = request.GET.getlist("sort", None)

    # Apply filters
    # TODO: if filtered/sorted on postdoc, then the year range is not limited to postdoc
    # so also alumni with PhD/MSc in the year range are shown
    if defence_year:
        multifilter = Q()
        for year in defence_year:
            end_year = str(int(year) + 10)
            if year == "1900":
                end_year = str(int(year) + 50)
            date_range=[year+"-01-01",end_year+"-01-01"]
            multifilter = multifilter | Q(degrees__date_of_defence__range=date_range)
            multifilter = multifilter | Q(positions__date_stop__range=date_range)
            multifilter = multifilter | Q(positions__date_start__range=date_range)
            multifilter = multifilter | Q(positions__date_stop__range=date_range)
            #multifilter = multifilter

            # print(Q(positions__date_stop__range=date_range))
            # print(Q(positions__date_start__range=date_range))
            # print(Q(positions__date_end__range=date_range))

        alumni = alumni.filter(multifilter).distinct()

    if degree_type:
        multifilter = Q()
        for degree in degree_type:
            multifilter = multifilter | Q(degrees__type=degree)

        alumni = alumni.filter(multifilter).distinct()

    # Sort the list
    if sort_on:
        if sort_on[0] == "alumnus_az":
            alumni = alumni.order_by("last_name")
        if sort_on[0] == "alumnus_za":
            alumni = alumni.order_by("-last_name")

        # Caution: sorting on degree/position implies filtering also
        if sort_on[0] == "msc_lh":
            alumni = alumni.filter(degrees__type__iexact="msc").distinct().order_by("degrees__date_of_defence")

        if sort_on[0] == "msc_hl":
            alumni = alumni.filter(degrees__type__iexact="msc").distinct().order_by("-degrees__date_of_defence")

        if sort_on[0] == "phd_lh":
            alumni = alumni.filter(degrees__type__iexact="phd").distinct().order_by("degrees__date_of_defence")
        if sort_on[0] == "phd_hl":
            alumni = alumni.filter(degrees__type__iexact="phd").distinct().order_by("-degrees__date_of_defence")

        if sort_on[0] == "pd_lh":
            alumni = alumni.filter(positions__type__name__in=["Postdoc",]).distinct().order_by("positions__date_stop")

        if sort_on[0] == "pd_hl":
            alumni = alumni.filter(positions__type__name__in=["Postdoc",]).distinct().order_by("positions__date_start")


        # if sort_on[0] == "pd_hl":
        #     alumni = alumni.filter(positions__type__name__in=["Postdoc",]).distinct().order_by("-positions__date_stop")

        # TODO: if an alumnus has several staff positions, then the latest date_stop must be returned.
        # Is this aggregating / grouping several tables together, then taking the max?
        if sort_on[0] == "staff_lh":
            alumni = alumni.filter(positions__type__name__in=["Full Professor", "Research Staff",
                "Adjunct Staff", "Faculty Staff"]).distinct().order_by("positions__date_stop")
        if sort_on[0] == "staff_hl":
            alumni = alumni.filter(positions__type__name__in=["Full Professor", "Research Staff",
                "Adjunct Staff", "Faculty Staff"]).distinct().order_by("positions__date_start")

        # if sort_on[0] == "staff_hl":
        #     alumni = alumni.filter(positions__type__name__in=["Full Professor", "Research Staff",
        #         "Adjunct Staff", "Faculty Staff"]).distinct().order_by("-positions__date_stop")



        if sort_on[0] == "obp_lh":
            alumni = alumni.filter(positions__type__name__in=["Instrumentation", "Institute Manager",
                "Outreach", "OBP", "Software Developer", "Nova" ]).distinct().order_by("positions__date_stop")

        if sort_on[0] == "obp_hl":
            alumni = alumni.filter(positions__type__name__in=["Instrumentation", "Institute Manager",
                "Outreach", "OBP", "Software Developer", "Nova" ]).distinct().order_by("positions__date_start")

        # if sort_on[0] == "obp_hl":
        #     alumni = alumni.filter(positions__type__name__in=["Instrumentation", "Institute Manager",
        #         "Outreach", "OBP", "Software Developer", "Nova" ]).distinct().order_by("-positions__date_stop")
    else:
        alumni = alumni.order_by("last_name")

    # TODO: only show unique results, though distinct on columns is not supported by sqlite3
    #alumni=alumni.distinct("last_name")
    # FIX: use python to uniqueify
    alumnus_unique = []
    for alumnus in alumni:
        if not alumnus in alumnus_unique:
            alumnus_unique.append(alumnus)

    alumni = alumnus_unique[:]

    # Paginate the list
    alumni_per_page = request.GET.get("limit", 15)

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
    page = request.GET.get("page", 1)

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


    return render(request, "alumni/alumnus_list.html", {"alumni": alumni, "alumni_per_page": int(alumni_per_page)})


def alumnus_detail(request, slug):
    alumnus = get_object_or_404(Alumnus, slug=slug)
    return render(request, "alumni/alumnus_detail.html", {"alumnus": alumnus})
