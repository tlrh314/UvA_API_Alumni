from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from .forms import SurveyForm

def survey_success(request):
	return render(request, "survey/thanks.html")


# Create your views here.
def survey(request):
	form_class = SurveyForm

#    contactinfo = SurveyForm.objects.all()
#    if contactinfo:
#        sent_to = contactinfo[0].secretary_email_address
#    else:
#        # Hardcoded in case ContactInfo has no instances.
#        sent_to = "secr-astro-science@uva.nl"

	if request.method == "POST":
		form = form_class(data=request.POST)
		print(form.is_valid())
		if form.is_valid():
			current_job = form.cleaned_data["current_job"]
			start_date_job = form.cleaned_data["start_date_job"]
			stop_date_job = form.cleaned_data["stop_date_job"]
			company_name = form.cleaned_data["company_name"]
			sector_job = form.cleaned_data["sector_job"]
			location_job = form.cleaned_data["location_job"]
			inside_academia = form.cleaned_data["inside_academia"]
			comments = form.cleaned_data["comments"]



			#name = form.cleaned_data["name"]
			#message = form.cleaned_data["message"]
			#sender = form.cleaned_data["sender"]
			#cc_myself = form.cleaned_data["cc_myself"]

            # recipients = ["timohalbesma@gmail.com"]  #  TODO: use sent_to
            # if cc_myself:
            #     recipients.append(sender)

			msg = "This message sent trough API Alumnus Website\n\n"
			msg += "Current job: {0}\n".format(current_job)
			msg += "start_date_job: {0}\n".format(start_date_job)
			msg += "stop_date_job: {0}\n".format(stop_date_job)
			msg += "company_name: {0}\n".format(company_name)
			msg += "sector_job: {0}\n".format(sector_job)
			msg += "-------------------------------------------------\n\n"
			msg += "{0}\n\n".format(comments)

			print(msg)
			#send_mail("Message sent trough API Alumnus Website", msg, sent_to, recipients)
			return HttpResponseRedirect("/survey/thanks/")
		else:
			print('notvalid')
	else:
		form = SurveyForm()

	return render(request, "survey/survey.html", {"form": form})