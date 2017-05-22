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


@login_required
def survey_contactinfo(request, use_for_main=False):
    """ Step 0 of the survey is a modified password reset url/template. Once the
        Alumnus has received a personal email with a tokened url to the modified
        password reset template, pressing 'next' on that password reset form leads
        here. This form surves the purpose to gather contact information, and
        on success this form then moves on to the survey_careerinfo view/form. """

    if request.method == "POST":
        form = SurveyContactInfoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("survey:careerinfo"))
    else:
        form = SurveyContactInfoForm(instance=request.user.alumnus)

    return render(request, "survey/survey_contactinfo.html", { "form": form,  })


@login_required
def survey_careerinfo(request):
    """ Career info form is shown on success of the survey_contactinfo view/form. """
    if request.method == "POST":
        form = SurveyCareerInfoForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("survey:survey_success"))
    else:
        form = SurveyCareerInfoForm(instance=request.user)

    return render(request, "survey/survey_careerinfo.html", { "form": form })


def survey_success(request):
    return render(request, "survey/survey_complete.html", {} )
