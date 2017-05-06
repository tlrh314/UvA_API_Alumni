from __future__ import unicode_literals, absolute_import, division

from django import template
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView

from .models import Alumnus, Degree

register = template.Library()

def alumnus_list(request):
    alumni = Alumnus.objects.all()

    # Get filters
    gender = request.GET.getlist('gender', None)
    defence_year = request.GET.getlist('year', None)

    # Apply filters
    if gender:
    	alumni = alumni.filter(gender=gender[0])

    if defence_year:
    	multifilter = Q()
    	for year in defence_year:

    		end_year = str(int(year) + 10)
    		date_range=[year+"-01-01",end_year+"-01-01"]
    		print(date_range)
    		multifilter = multifilter | Q(degrees__date_of_defence__range=date_range)
    		multifilter = multifilter | Q(degrees__date_stop__range=date_range)

    	alumni = alumni.filter(multifilter)
    		# alumni = alumni.filter(degrees__date_of_defence__range=date_range)

    # Degree.objects.all()
    # if defence:
    	# alumni = alumni.filter(degrees.date_of_defence=defence)


    # print(alumni[0].GENDER_CHOICES)

    # defence_years = alumni.
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
