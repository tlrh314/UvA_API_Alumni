# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division

from datetime import datetime

from django import forms
from django.template import loader
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


from django_countries import countries
# from django_countries.widgets import CountrySelectWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Sector
from .models import JobAfterLeaving
from ..alumni.models import Alumnus


class SendSurveyForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    # Here we overwrite the save method because the PasswordResetForm gets
    # all users given an e-mail address, but we want to e-mail one specific
    # alumnus only once. This avoids sending the same mail multiple times.
    # Also, here we set the templates to use for the subject and e-mail.
    # Based on Django 1.11, if Django is upgraded: check changes to PasswordResetForm
    def save(self, alumnus, domain_override=None,
             subject_template_name="survey/survey_email_subject.txt",
             email_template_name="survey/send_survey_email.html",
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            "email": email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(alumnus.user.pk)).decode(),
            "user": alumnus.user,
            "token": token_generator.make_token(alumnus.user),
            "protocol": "https" if use_https else "http",
        }
        if extra_email_context is not None:
            context.update(extra_email_context)
        self.send_mail(
            subject_template_name, email_template_name, context, from_email,
            email, html_email_template_name=html_email_template_name,
        )

class SurveyContactInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyContactInfoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse("survey:contactinfo")
        self.helper.form_class = "form-horizontal col-xs-12"
        self.helper.layout.append(Submit("survey_careerinfo", "Next", css_class="btn btn-success pull-right"))

    class Meta:
        model = Alumnus
        # fields = ()
        exclude = ("user", "last_name", "show_person", "passed_away", "nickname", "student_id",
                    "mugshot", "slug" , "email", "last_checked", "position", "specification",
                    "office", "work_phone", "ads_name", "research", "contact",
                    "comments", "date_created", "date_updated", "last_updated_by")


class SurveyCareerInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyCareerInfoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse("survey:careerinfo")
        self.helper.form_class = "form-horizontal col-xs-12"
        self.helper.layout.append(Submit("survey_contactinfo", "Submit", css_class="btn btn-success pull-right"))

    class Meta:
        model = JobAfterLeaving
        exclude = ("alumnus", "date_created", "date_updated", "last_updated_by")

