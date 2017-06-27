# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division

import copy

from datetime import datetime
from django import forms
from django.forms import extras
from django.forms.utils import ErrorList
from django.template import loader
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.fields import BLANK_CHOICE_DASH

from django_countries import countries
from tinymce.widgets import TinyMCE

from .models import Sector
from .models import JobAfterLeaving
from ..alumni.models import Alumnus
from ..alumni.models import AcademicTitle
from ...settings import TINYMCE_MINIMAL_CONFIG

error_messages = {
    "names": "Names cannot contain numbers",
    "numbers": "Phonenumbers can only contain numbers",
    "initials": "Initials can only contain letters"
}

TINYMCE_LOCAL_CONFIG= {
    'selector': 'textarea',
    'height': 200,
    'width': 0,
    'menubar': False,
    'statusbar': False,
    'elementpath': False,
    'plugins': [
        'paste',
    ],
    'toolbar1': 'undo redo | bold italic | bullist numlist outdent indent | ',
    'toolbar2': '',
    'paste_as_text': True,
}


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
            "uid": urlsafe_base64_encode(force_bytes(alumnus.pk)).decode(),
            "user": alumnus,
            "token": token_generator.make_token(alumnus),
            "protocol": "https" if use_https else "http",
        }
        if extra_email_context is not None:
            context.update(extra_email_context)
        self.send_mail(
            subject_template_name, email_template_name, context, from_email,
            email, html_email_template_name=html_email_template_name,
        )


class SurveyCareerInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyCareerInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JobAfterLeaving
        exclude = ("alumnus", "date_created", "date_updated", "last_updated_by", "which_position")


    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    years_choices = range(1900, datetime.now().year+10)[::-1]

    sector = forms.ModelChoiceField(
        required=False,
        queryset=Sector.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}))

    company_name = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    position_name = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    is_inside_academia = forms.ChoiceField(
        required=False,
        choices=JobAfterLeaving.YES_OR_NO,
        widget=forms.Select(
            attrs={"class": "form-control"}))

    location_job = forms.ChoiceField(
        required=False,
        choices=BLANK_CHOICE_DASH+list(countries),
        widget=forms.Select(
            attrs={"class": "form-control"}))

    start_date = forms.DateField(
        required=False,
        widget=extras.SelectDateWidget(
            years=years_choices,
            attrs={"class":"datetime-input"})
        )

    stop_date = forms.DateField(
        required=False,
        widget=extras.SelectDateWidget(
            years=years_choices,
            attrs={"class":""}))

    comments = forms.CharField(
        required=False,
        widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG)
    )

    show_job = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    def clean(self):
        position_name = self.cleaned_data.get("position_name")
        if any(str.isdigit(c) for c in position_name):
            self._errors["position_name"] = ErrorList()
            self._errors["position_name"].append(error_messages["names"])

class SurveyContactInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyContactInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Alumnus
        exclude = ("user", "show_person", "passed_away", "nickname", "student_id",
                    "mugshot", "slug", "last_checked", "position", "specification",
                    "office", "work_phone", "ads_name", "research", "contact",
                    "comments", "date_created", "date_updated", "last_updated_by",
                    "zipcode", "streetname", "streetnumber", "address",
                    # Below has to be removed b/c Alumnus is an extension of AbstractBaseUser
                    "password", "last_login", "is_superuser", "groups",
                    "user_permissions", "username", "is_staff", "is_active", "date_joined")

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    years_choices = range(1900, datetime.now().year+1)[::-1]

    academic_title = forms.ModelChoiceField(
        required=False,
        queryset=AcademicTitle.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}))

    initials = forms.CharField(
        required=False,
        help_text="Please use letters only, no dots",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    first_name = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    middle_names = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    prefix = forms.CharField(
        required=False,
        help_text="Tussenvoegsel, e.g. 'van der', 'de'",
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    last_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    gender = forms.ChoiceField(
        required=False,
        choices=Alumnus.GENDER_CHOICES,
        widget=forms.Select(
            attrs={"class": "form-control"}))

    birth_date = forms.DateField(
        required=False,
        widget=extras.SelectDateWidget(
            years=years_choices,
            attrs={"class":""}))

    nationality = forms.ChoiceField(
        required=False,
        choices=BLANK_CHOICE_DASH+list(countries),
        widget=forms.Select(
            attrs={"class": "form-control"}))

    place_of_birth = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    mugshot = forms.ImageField(
        required=False)

    biography = forms.CharField(
        required=False,
        max_length=2048,
        widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG))

    show_biography = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
            attrs={"class":"form-control"}))

    show_email = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    home_phone = forms.CharField(
        required=False,
        help_text="Please use digits only",
        max_length=24,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    mobile = forms.CharField(
        required=False,
        help_text="Please use digits only",
        max_length=24,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    homepage = forms.URLField(
        required=False,
        help_text="Please give the full URL to your homepage",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    show_homepage = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    facebook = forms.URLField(
        required=False,
        help_text="Please give the full URL to your Facebook",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    show_facebook = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    twitter = forms.URLField(
        required=False,
        help_text="Please give the full URL to your Twitter",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    show_twitter = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    linkedin = forms.URLField(
        required=False,
        help_text="Please give the full URL to LinkedIn",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    show_linkedin = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"class":"form-control"}))

    city = forms.CharField(
        required=False,
        max_length=24,
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    country = forms.ChoiceField(
        required=False,
        choices=BLANK_CHOICE_DASH+list(countries),
        widget=forms.Select(
            attrs={"class": "form-control"}))

    field_order= [
            "academic_title", "initials", "first_name", "middle_names",
            "prefix", "last_name", "gender", "birth_date",  "nationality",
            "place_of_birth", "mugshot", "biography", "show_biography", "email",
            "show_email", "home_phone", "mobile", "homepage", "show_homepage",
            "facebook", "show_facebook", "twitter","show_twitter", "linkedin",
            "show_linkedin", "city", "country" ]


    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        if any(str.isdigit(c) for c in first_name):
            self._errors["first_name"] = ErrorList()
            self._errors["first_name"].append(error_messages["names"])

        middle_names = self.cleaned_data.get("middle_names")
        if any(str.isdigit(c) for c in middle_names):
            self._errors["middle_names"] = ErrorList()
            self._errors["middle_names"].append(error_messages["names"])

        initials = self.cleaned_data.get("initials")
        if initials and not initials.isalpha():
            self._errors["initials"] = ErrorList()
            self._errors["initials"].append(error_messages["initials"])

        prefix = self.cleaned_data.get("prefix")
        if any(str.isdigit(c) for c in prefix):
            self._errors["prefix"] = ErrorList()
            self._errors["prefix"].append(error_messages["names"])

        # TODO: Expand to english prefixes too
        allowed_prefix = ["van", "van der", "der", "den", "van den", "van de", "de", "in het", "in 't", "di"]
        if prefix and prefix not in allowed_prefix:
            self._errors["prefix"] = ErrorList()
            self._errors["prefix"].append("Valid options: {0}".format(allowed_prefix))

        place_of_birth = self.cleaned_data.get("place_of_birth")
        if any(str.isdigit(c) for c in place_of_birth):
            self._errors["place_of_birth"] = ErrorList()
            self._errors["place_of_birth"].append(error_messages["names"])

        city = self.cleaned_data.get("city")
        if any(str.isdigit(c) for c in city):
            self._errors["city"] = ErrorList()
            self._errors["city"].append(error_messages["names"])

        home_phone = self.cleaned_data.get("home_phone")
        if home_phone and not home_phone.isdigit():
           self._errors["home_phone"] = ErrorList()
           self._errors["home_phone"].append(error_messages["numbers"])

        mobile = self.cleaned_data.get("mobile")
        if mobile and not mobile.isdigit():
           self._errors["mobile"] = ErrorList()
           self._errors["mobile"].append(error_messages["numbers"])
