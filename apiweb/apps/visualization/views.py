from django.http import Http404
from django.db.models import Count
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

import json

from ..alumni.models import Alumnus
from ..research.models import Thesis
from ..survey.models import JobAfterLeaving


def view_a(request):
    """
    View to display whether the 1,2,3rd job outside api is within or outside the field of astronomy
    """

    data_dict, data_dict_cur, data_dict_1, data_dict_2, data_dict_3 = {}, {}, {}, {}, {}

    fieldname = 'is_inside_astronomy'

    jobs_all = JobAfterLeaving.objects.all()
    jobs_in_astronomy = jobs_all.exclude(is_inside_astronomy=None)

    jobs_cur = jobs_in_astronomy.filter(which_position=0)
    jobs_1 = jobs_in_astronomy.filter(which_position=1)
    jobs_2 = jobs_in_astronomy.filter(which_position=2)
    jobs_3 =jobs_in_astronomy.filter(which_position=3)

    astronomy_counts_cur = jobs_cur.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in astronomy_counts_cur:
        data_dict_cur[el[fieldname]] = el['amount']

    astronomy_counts_1 = jobs_1.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in astronomy_counts_1:
        data_dict_1[el[fieldname]] = el['amount']
    
    astronomy_counts_2 = jobs_2.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in astronomy_counts_2:
        data_dict_2[el[fieldname]] = el['amount']
    
    astronomy_counts_3 = jobs_3.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in astronomy_counts_3:
        data_dict_3[el[fieldname]] = el['amount']

    data_dict['jobs_cur'] = data_dict_cur
    data_dict['jobs_1'] = data_dict_1
    data_dict['jobs_2'] = data_dict_2
    data_dict['jobs_3'] = data_dict_3
    #print data_dict

    json_data = json.dumps(data_dict)

    return render(request, "visualization/vis_a.html", {'json_data': json_data})

def view_b(request):
    """
    View to the location of the 1,2,3rd job (NL, eu..)
    """
    
    data_dict, data_dict_cur, data_dict_1, data_dict_2, data_dict_3 = {}, {}, {}, {}, {}

    fieldname = 'location_job'
    jobs_all = JobAfterLeaving.objects.all() 
    jobs_with_location = jobs_all.exclude(location_job='')
    
    jobs_cur = jobs_with_location.filter(which_position=0)
    jobs_1 = jobs_with_location.filter(which_position=1)
    jobs_2 = jobs_with_location.filter(which_position=2)
    jobs_3 =jobs_with_location.filter(which_position=3)

    location_counts_cur = jobs_cur.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in location_counts_cur:
        data_dict_cur[el[fieldname]] = el['amount']

    location_counts_1 = jobs_1.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in location_counts_1:
        data_dict_1[el[fieldname]] = el['amount']
    
    location_counts_2 = jobs_2.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in location_counts_2:
        data_dict_2[el[fieldname]] = el['amount']
    
    location_counts_3 = jobs_3.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in location_counts_3:
        data_dict_3[el[fieldname]] = el['amount']

    data_dict['jobs_cur'] = data_dict_cur
    data_dict['jobs_1'] = data_dict_1
    data_dict['jobs_2'] = data_dict_2
    data_dict['jobs_3'] = data_dict_3
    #print data_dict

    json_data = json.dumps(data_dict)
    return render(request, "visualization/vis_b.html", {'json_data': json_data})

def view_c(request):
    """
    View to visualize, if the job is in the field of astronomy, whether it is at a university, or a different institute type
    """
    pass

def view_d(request):
    """
    View to visualize, if not inside field of astronomy, which sector the job is in.
    """
    data_dict, data_dict_cur, data_dict_1, data_dict_2, data_dict_3 = {}, {}, {}, {}, {}

    fieldname = 'sector__name'
    jobs_all = JobAfterLeaving.objects.all() 
    jobs_with_sector = jobs_all.exclude(sector=None)
    
    sector_cur = jobs_with_sector.filter(which_position=0)
    sector_1 = jobs_with_sector.filter(which_position=1)
    sector_2 = jobs_with_sector.filter(which_position=2)
    sector_3 = jobs_with_sector.filter(which_position=3)

    sector_counts_cur = sector_cur.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in sector_counts_cur:
        data_dict_cur[el[fieldname]] = el['amount']

    sector_counts_1 = sector_1.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in sector_counts_1:
        data_dict_1[el[fieldname]] = el['amount']
    
    sector_counts_2 = sector_2.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in sector_counts_2:
        data_dict_2[el[fieldname]] = el['amount']
    
    sector_counts_3 = sector_3.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in sector_counts_3:
        data_dict_3[el[fieldname]] = el['amount']

    data_dict['sector_cur'] = data_dict_cur
    data_dict['sector_1'] = data_dict_1
    data_dict['sector_2'] = data_dict_2
    data_dict['sector_3'] = data_dict_3
    print (data_dict)

    json_data = json.dumps(data_dict)
    return render(request, "visualization/vis_d.html", {'json_data': json_data})

def view_e(request):
    """
    What is the land of origin of the alumni
    """

    data_dict = {}
    fieldname = 'country'

    alumni = Alumnus.objects.all()    
    alumni_with_country = alumni.exclude(country='')
    
    country_counts = alumni_with_country.values(fieldname).order_by(fieldname).annotate(amount=Count(fieldname))
    for el in country_counts:
        data_dict[el['country']] = el['amount']
        
    json_data = json.dumps(data_dict)
    return render(request, "visualization/vis_e.html", {'json_data': json_data})

def view_f(request):
    """
    What is the gender of the alumnus?
    """

    data_dict = {}

    alumni = Alumnus.objects.all()
    alumni_with_gender = alumni.exclude(gender=None)
    alumni_male = alumni_with_gender.filter(gender=1)
    alumni_female = alumni_with_gender.filter(gender=2)
    alumni_other = alumni_with_gender.filter(gender=3)
    alumni_not_say = alumni_with_gender.filter(gender=4)

    data_dict['male'] = alumni_male.count()
    data_dict['female'] = alumni_female.count()
    data_dict['other'] = alumni_other.count()
    data_dict['rather_not_say'] = alumni_not_say.count()

    json_data = json.dumps(data_dict)
    return render(request, "visualization/vis_f.html", {'json_data': json_data})


def tree(request):
    # phd_theses = Thesis.objects.filter(type="phd").order_by("date_of_defence")
    # msc_theses = Thesis.objects.filter(type="msc").order_by("date_of_defence")

    theses = Thesis.objects.exclude(advisor=None)

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
            link_dict["data"]["thesis_url"] = thesis.get_absolute_url()
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
        node_dict["data"]["alumnus_url"] = alumnus.get_absolute_url()
        nodes_list.append(node_dict)

    data_dict["nodes"] = nodes_list
    data_dict["edges"] = links_list

    json_data = json.dumps(data_dict)
    return render(request, "visualization/tree3.html", {'json_data': json_data})