from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

from .forms import SurveyContactInfoForm
from .forms import SurveyCareerInfoForm


#TODO: make sure they are redirected to the correct page
@login_required 
def survey_contactinfo(request):
    """ Step 0 of the survey is a modified password reset url/template. Once the
        Alumnus has received a personal email with a tokened url to the modified
        password reset template, pressing 'next' on that password reset form leads
        here. This form surves the purpose to gather contact information, and
        on success this form then moves on to the survey_careerinfo view/form. """

    if request.method == "POST":
        form = SurveyContactInfoForm(data=request.POST)
        form.is_valid()  # TODO: remove

        # TODO: if user is annonymous, then handle form differently then when Alumnus is know (which is when user is logged in)
        # TODO: get alumus. Should be request.user.alumnus

        if form.is_valid():
            # TODO: check and clean, then save only the fields that are not empty into the Alumnus?

            academic_title              = form.cleaned_data["academic_title"]
            initials                    = form.cleaned_data["initials"]
            first_name                  = form.cleaned_data["first_name"]
            middle_names                = form.cleaned_data["middle_names"]
            prefix                      = form.cleaned_data["prefix"] 
            gender                      = form.cleaned_data["gender"]
            birth_date                  = form.cleaned_data["birth_date"] 
            nationality                 = form.cleaned_data["nationality"]
            place_of_birth              = form.cleaned_data["place_of_birth"]
            #photo                      = form.cleaned_data["photo"]
            biography                   = form.cleaned_data["biography"] 
            home_phone                  = form.cleaned_data["home_phone"]
            mobile                      = form.cleaned_data["mobile"]
            homepage                    = form.cleaned_data["homepage"] 
            facebook                    = form.cleaned_data["facebook"]
            twitter                     = form.cleaned_data["twitter"]
            linkedin                    = form.cleaned_data["linkedin"] 
            city                        = form.cleaned_data["city"]
            country                     = form.cleaned_data["country"] 

            msg = ""
            msg += "academic_title          = {0}\n".format(academic_title)
            msg += "initials                = {0}\n".format(initials)
            msg += "first_name              = {0}\n".format(first_name)
            msg += "middle_names            = {0}\n".format(middle_names)
            msg += "prefix                  = {0}\n".format(prefix)
            msg += "gender                  = {0}\n".format(gender)
            msg += "birth_date              = {0}\n".format(birth_date)
            msg += "nationality             = {0}\n".format(nationality)
            msg += "place_of_birth          = {0}\n".format(place_of_birth)
            msg += "biography               = {0}\n".format(biography)            
            msg += "home_phone              = {0}\n".format(home_phone)   
            msg += "mobile                  = {0}\n".format(mobile) 
            msg += "homepage                = {0}\n".format(homepage) 
            msg += "facebook                = {0}\n".format(facebook) 
            msg += "twitter                 = {0}\n".format(twitter)
            msg += "linkedin                = {0}\n".format(linkedin)
            msg += "city                    = {0}\n".format(city)
            msg += "country                 = {0}\n".format(country)
            msg += "twitter                 = {0}\n".format(twitter)
            print(msg)

            return HttpResponseRedirect(reverse("survey:careerinfo"))
    else:
        form = SurveyContactInfoForm(instance=request.user.alumnus)

    return render(request, "survey/survey_contactinfo.html", { "form": form,  })

#TODO: make sure they are sent to the correct page
@login_required
def survey_careerinfo(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """

    if request.method == "POST":
        form = SurveyCareerInfoForm(data=request.POST)

        # TODO: if user is annonymous, then handle form differently then when Alumnus is know (which is when user is logged in)
        # TODO: get alumus. Should be request.user.alumnus

        form.is_valid()  # TODO: remove
        if form.is_valid():
            # TODO: check and clean, then save only the fields that are not empty into the Alumnus?
            # TODO: get alumus. Should be request.user.alumnus
            sector                     = form.cleaned_data["sector"]
            company_name               = form.cleaned_data["company_name"]
            position_name              = form.cleaned_data["position_name"]
            is_current_job             = form.cleaned_data["is_current_job"]
            is_inside_academia         = form.cleaned_data["is_inside_academia"]
            location_job               = form.cleaned_data["location_job"]
            start_date                 = form.cleaned_data["start_date"]
            stop_date                  = form.cleaned_data["stop_date"]

            msg = ""
            msg += "sector             = {0}\n".format(sector)
            msg += "company_name       = {0}\n".format(company_name)
            msg += "position_name      = {0}\n".format(position_name)
            msg += "is_current_job     = {0}\n".format(is_current_job)
            msg += "is_inside_academia = {0}\n".format(is_inside_academia)
            msg += "location_job       = {0}\n".format(location_job)
            msg += "start_date         = {0}\n".format(start_date)
            msg += "stop_date          = {0}\n".format(stop_date)

            print(msg)
            return HttpResponseRedirect(reverse("survey:survey_success"))
    else:
        form = SurveyCareerInfoForm(instance=request.user)

    return render(request, "survey/survey_careerinfo.html", { "form": form })


def survey_success(request):
    return render(request, "survey/survey_complete.html", {} )
