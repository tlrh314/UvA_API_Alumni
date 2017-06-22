from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SurveyContactInfoForm
from .forms import SurveyCareerInfoForm

from .models import JobAfterLeaving


@login_required
def survey_contactinfo(request, use_for_main=False):
    """ Step 0 of the survey is a modified password reset url/template. Once the
        Alumnus has received a personal email with a tokened url to the modified
        password reset template, pressing 'next' on that password reset form leads
        here. This form surves the purpose to gather contact information, and
        on success this form then moves on to the survey_careerinfo view/form. """
    if request.method == "POST":
        form = SurveyContactInfoForm(data=request.POST, instance=request.user.alumnus, files=request.FILES)
        if form.is_valid():
            alumnus = form.save(commit=False)
            alumnus.user = request.user
            alumnus.save()
            return HttpResponseRedirect(reverse("survey:careerinfo_current"))
    else:
        form = SurveyContactInfoForm(instance=request.user.alumnus)

    return render(request, "survey/survey_contactinfo.html", { "form": form,  })


@login_required
def survey_careerinfo_current(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 0
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(alumnus=request.user.alumnus,which_position=which_position_value)[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if "finish" in request.POST:
            messages.success(request, "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.alumnus.slug}))

        # TODO: this if statement is not necessary if prefill_instance is set to None in the try-expect clause above.
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user.alumnus
            jobafterleaving.which_position = which_position_value
            jobafterleaving.save()
            return HttpResponseRedirect(reverse("survey:careerinfo_first"))
    else:
        # TODO: this if statement is not necessary if prefill_instance is set to None in the try-expect clause above.
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_current.html", { "form": form })



@login_required
def survey_careerinfo_first(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 1
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(alumnus=request.user.alumnus,which_position=which_position_value)[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if "finish" in request.POST:
            messages.success(request, "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.alumnus.slug}))
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user.alumnus
            jobafterleaving.which_position = which_position_value
            jobafterleaving.save()
            return HttpResponseRedirect(reverse("survey:careerinfo_second"))
    else:
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_first.html", { "form": form })

@login_required
def survey_careerinfo_second(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 2
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(alumnus=request.user.alumnus,which_position=which_position_value)[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if "finish" in request.POST:
            messages.success(request, "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.alumnus.slug}))
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user.alumnus
            jobafterleaving.which_position = which_position_value
            jobafterleaving.save()
            return HttpResponseRedirect(reverse("survey:careerinfo_third"))
    else:
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_second.html", { "form": form })



@login_required
def survey_careerinfo_third(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 3
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(alumnus=request.user.alumnus,which_position=which_position_value)[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user.alumnus
            jobafterleaving.which_position = which_position_value
            jobafterleaving.save()
            messages.success(request, "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.alumnus.slug}))
    else:
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_third.html", { "form": form })

def survey_success(request):
    return render(request, "survey/survey_complete.html", {} )
