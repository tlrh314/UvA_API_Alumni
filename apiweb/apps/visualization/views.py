

from django.http import Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

import json

from ..alumni.models import Alumnus
from ..research.models import Thesis


def tree(request):
    # phd_theses = Thesis.objects.filter(type="phd").order_by("date_of_defence")
    # msc_theses = Thesis.objects.filter(type="msc").order_by("date_of_defence")

    theses = Thesis.objects.all().order_by("date_of_defence")
    data_dict = {}
    links_list, nodes_list, all_people = [], [], []

    #Get all thesis, students and advisors for phd
    for thesis in theses:
        student = thesis.alumnus

        for i, supervisor in enumerate(thesis.advisor.all()):
            if not supervisor in all_people:
                all_people.append(supervisor)

            link_dict = {"data": {}}
            link_dict["data"]["source"] = str(supervisor.last_name.replace("'"," "))
            link_dict["data"]["target"] = str(student.last_name.replace("'"," "))
            link_dict["data"]["type"] = thesis.type
            link_dict["strength"] = 1
            links_list.append(link_dict)

        if not student in all_people:
            all_people.append(student)

    #Get all the nodes
    for alumnus in all_people:
        node_dict = {"data": {}}
        node_dict["data"]["id"] = str(alumnus.last_name.replace("'"," "))
        # node_dict["group"] = i+1
        node_dict["data"]["weight"] = alumnus.students.count() + 1
        nodes_list.append(node_dict)

    data_dict["nodes"] = nodes_list
    data_dict["edges"] = links_list

    json_data = json.dumps(data_dict)
    return render(request, "visualization/tree3.html", {'json_data': json_data})



def tree_msc(request):
    phd_theses = Thesis.objects.filter(type="phd").order_by("date_of_defence")
    msc_theses = Thesis.objects.filter(type="msc").order_by("date_of_defence")

    data_dict = {}
    links_list, nodes_list, all_people = [], [], []

    #Get all thesis, students and advisors for phd
    for thesis in msc_theses:
        student = thesis.alumnus
        amt_supervisors = 0

        for i, supervisor in enumerate(thesis.advisor.all()):
            if not supervisor in all_people:
                all_people.append(supervisor)

            link_dict = {}
            link_dict["source"] = str(supervisor.last_name.replace("'"," "))
            link_dict["target"] = str(student.last_name.replace("'"," "))
            link_dict["value"] = i+1
            links_list.append(link_dict)

            amt_supervisors = i+1

        #With the first condition, we skip all those who have not yet a supervisor assigned to them
        if not amt_supervisors == 0:
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

    json_data = json.dumps(data_dict)
    return render(request, "visualization/tree_msc.html", {'json_data': json_data})


def nationality(request):
    alumni = Alumnus.objects.all().exclude(nationality='')

    return render(request, "visualization/tree2.html")


def tree2(request):
    return render(request, "visualization/tree2.html")
