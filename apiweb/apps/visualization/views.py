from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

import json

from ..alumni.models import Alumnus
from ..alumni.models import Degree


def tree(request):
    phd_theses = Degree.objects.filter(type="phd").order_by("date_of_defence")
    msc_theses = Degree.objects.filter(type="msc").order_by("date_of_defence")

    data_dict = {}
    links_list, nodes_list, all_people = [], [], []

    #Get all thesis, students and advisors for phd
    for thesis in phd_theses:
        student = thesis.alumnus
                
        for i, supervisor in enumerate(thesis.thesis_advisor.all()):
            if not supervisor in all_people:
                all_people.append(supervisor)
            
            link_dict = {}
            link_dict["source"] = str(supervisor.last_name.replace("'"," "))
            link_dict["target"] = str(student.last_name.replace("'"," "))
            link_dict["value"] = i+1
            links_list.append(link_dict)
        
        if not student in all_people:
            all_people.append(student)

    #Get all the nodes
    for alumnus in all_people:
        node_dict = {}
        node_dict["id"] = str(alumnus.last_name.replace("'"," "))
        node_dict["group"] = i+1
        nodes_list.append(node_dict)
    
    data_dict["nodes"] = nodes_list
    data_dict["links"] = links_list

    with open('json_content_phd.json', 'w') as outfile:
        json.dump(data_dict, outfile)

    json_data = json.dumps(data_dict)

    return render(request, "visualization/tree.html", {'json_data': json_data})

def tree2(request):
    return render(request, "visualization/tree2.html")
