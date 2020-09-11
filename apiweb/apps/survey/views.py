from __future__ import absolute_import, division, unicode_literals

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from .forms import SurveyCareerInfoForm, SurveyContactInfoForm
from .models import JobAfterLeaving


@login_required
def survey_contactinfo(request, use_for_main=False):
    """ Step 0 of the survey is a modified password reset url/template. Once the
        Alumnus has received a personal email with a tokened url to the modified
        password reset template, pressing 'next' on that password reset form leads
        here. This form surves the purpose to gather contact information, and
        on success this form then moves on to the survey_careerinfo view/form. """
    if request.method == "POST":
        form = SurveyContactInfoForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            alumnus = form.save(commit=False)
            alumnus.user = request.user
            alumnus.save()
            return HttpResponseRedirect(reverse("survey:careerinfo_current"))
    else:
        form = SurveyContactInfoForm(instance=request.user)

    return render(request, "survey/survey_contactinfo.html", {"form": form,})


@login_required
def survey_careerinfo_current(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 0
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(
            alumnus=request.user, which_position=which_position_value
        )[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if "finish" in request.POST:
            messages.success(
                request,
                "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.",
            )
            return HttpResponseRedirect(
                reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
            )

        # TODO: this if statement is not necessary if prefill_instance is set to None in the try-expect clause above.
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user
            jobafterleaving.which_position = which_position_value
            jobafterleaving.alumnus.survey_info_updated = datetime.now()
            jobafterleaving.alumnus.save()
            print("survey, cur %s" % jobafterleaving.alumnus.survey_info_updated)
            jobafterleaving.save()
            if "next" in request.POST:
                return HttpResponseRedirect(reverse("survey:careerinfo_first"))
            elif "prev" in request.POST:
                return HttpResponseRedirect(reverse("survey:contactinfo"))
    else:
        # TODO: this if statement is not necessary if prefill_instance is set to None in the try-expect clause above.
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_current.html", {"form": form})


@login_required
def survey_careerinfo_first(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 1
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(
            alumnus=request.user, which_position=which_position_value
        )[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if "finish" in request.POST:
            messages.success(
                request,
                "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.",
            )
            return HttpResponseRedirect(
                reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
            )
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user
            jobafterleaving.which_position = which_position_value
            jobafterleaving.alumnus.survey_info_updated = datetime.now()
            jobafterleaving.alumnus.save()
            print("survey, 1 %s" % jobafterleaving.alumnus.survey_info_updated)
            jobafterleaving.save()
            if "next" in request.POST:
                return HttpResponseRedirect(reverse("survey:careerinfo_second"))
            elif "prev" in request.POST:
                return HttpResponseRedirect(reverse("survey:careerinfo_current"))
    else:
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_first.html", {"form": form})


@login_required
def survey_careerinfo_second(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 2
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(
            alumnus=request.user, which_position=which_position_value
        )[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if "finish" in request.POST:
            messages.success(
                request,
                "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.",
            )
            return HttpResponseRedirect(
                reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
            )
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user
            jobafterleaving.which_position = which_position_value
            jobafterleaving.alumnus.survey_info_updated = datetime.now()
            jobafterleaving.alumnus.save()
            print("survey, 2 %s" % jobafterleaving.alumnus.survey_info_updated)
            jobafterleaving.save()

            if "next" in request.POST:
                return HttpResponseRedirect(reverse("survey:careerinfo_third"))
            if "prev" in request.POST:
                return HttpResponseRedirect(reverse("survey:careerinfo_first"))
    else:
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_second.html", {"form": form})


@login_required
def survey_careerinfo_third(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    which_position_value = 3
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(
            alumnus=request.user, which_position=which_position_value
        )[0]
    except IndexError:
        prefill_instance = False

    if request.method == "POST":
        if prefill_instance:
            form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user
            jobafterleaving.which_position = which_position_value
            jobafterleaving.alumnus.survey_info_updated = datetime.now()
            jobafterleaving.alumnus.save()
            print("survey, 3 %s" % jobafterleaving.alumnus.survey_info_updated)
            jobafterleaving.save()
            messages.success(
                request,
                "Thanks for taking the time to fill out our survey! Welcome to your personal alumnus page.",
            )

            if "next" in request.POST:
                return HttpResponseRedirect(
                    reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
                )
            elif "prev" in request.POST:
                return HttpResponseRedirect(reverse("survey:careerinfo_second"))
    else:
        if prefill_instance:
            form = SurveyCareerInfoForm(instance=prefill_instance)
        else:
            form = SurveyCareerInfoForm()
    return render(request, "survey/survey_careerinfo_third.html", {"form": form})


@login_required
def survey_success(request):
    return render(request, "survey/survey_complete.html", {})
