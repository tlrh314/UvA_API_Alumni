from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from ..alumni.models import Alumnus
from ..alumni.models import Degree

def tree(request):
    phd_theses = Degree.objects.filter(type="phd").order_by("date_of_defence")
    msc_theses = Degree.objects.filter(type="msc").order_by("date_of_defence")

    # Create id for every
    # for i, supervisor in enumerate(Alumnus.objects.filter(students__isnull=False).distinct()):


    print('{\n  "nodes": [')
    for i, supervisor in enumerate(Alumnus.objects.filter(students__isnull=False).distinct()):
        print('    {"id": "'+supervisor.last_name+'", "group": '+str(i+1)+'},')
    print('  ],\n  "links": [')

    for thesis in phd_theses:
        student = thesis.alumnus.last_name
        for i, supervisor in enumerate(thesis.thesis_advisor.all()):
            # print('{"id":'+'"{}", "{}"'.format(student, supervisor))
            print('    {"source": "'+supervisor.last_name+'", "target": "'+student+'", "value": '+str(i+1)+'},')
    print('  ]\n}')





    return render(request, "visualization/tree.html")


def tree2(request):
    return render(request, "visualization/tree2.html")
