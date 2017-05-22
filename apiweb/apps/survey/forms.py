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


class SurveyCareerInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyCareerInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JobAfterLeaving
        exclude = ("alumnus", "date_created", "date_updated", "last_updated_by")

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

    is_current_job = forms.ChoiceField(
        required=False,
        choices=JobAfterLeaving.YES_OR_NO,
        widget=forms.Select(
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
            attrs={"class":""}))

    stop_date = forms.DateField(
        required=False,
        widget=extras.SelectDateWidget(
            years=years_choices,
            attrs={"class":""}))

    comments = forms.CharField(
        required=False,
        widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG)
    )

    def clean(self):
        """
        Clean function for input
        """

        position_name = self.cleaned_data.get("position_name")
        if any(str.isdigit(c) for c in position_name):
            self._errors["position_name"] = ErrorList()
            self._errors["position_name"].append(error_messages["names"])

    def save(self):
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
        comments                   = form.cleaned_data["comments"]

        msg = ""
        msg += "sector             = {0}\n".format(sector)
        msg += "company_name       = {0}\n".format(company_name)
        msg += "position_name      = {0}\n".format(position_name)
        msg += "is_current_job     = {0}\n".format(is_current_job)
        msg += "is_inside_academia = {0}\n".format(is_inside_academia)
        msg += "location_job       = {0}\n".format(location_job)
        msg += "start_date         = {0}\n".format(start_date)
        msg += "stop_date          = {0}\n".format(stop_date)
        msg += "comments           = {0}\n".format(comments)

        variable_list = [sector, company_name, position_name, is_current_job, is_inside_academia, location_job, start_date, stop_date, comments]
        for var in variable_list:
            if var: print(len(var))

        print(msg)


class SurveyContactInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyContactInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Alumnus
        exclude = ("user", "last_name", "show_person", "passed_away", "nickname", "student_id",
                    "mugshot", "slug", "last_checked", "position", "specification",
                    "office", "work_phone", "ads_name", "research", "contact",
                    "comments", "date_created", "date_updated", "last_updated_by",
                    "zipcode", "streetname", "streetnumber", "address")

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

    photo = forms.ImageField(
        required=False)

    biography = forms.CharField(
        required=False,
        max_length=2048,
        widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG))

    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
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

    facebook = forms.URLField(
        required=False,
        help_text="Please give the full URL to your Facebook",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    twitter = forms.URLField(
        required=False,
        help_text="Please give the full URL to your Twitter",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

    linkedin = forms.URLField(
        required=False,
        help_text="Please give the full URL to LinkedIn",
        widget=forms.TextInput(
            attrs={"class": "form-control"}))

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

    def clean(self):
        #first names cleaner
        first_name = self.cleaned_data.get("first_name")
        if any(str.isdigit(c) for c in first_name):
            self._errors["first_name"] = ErrorList()
            self._errors["first_name"].append(error_messages["names"])

        #middle names cleaneer
        middle_names = self.cleaned_data.get("middle_names")
        if any(str.isdigit(c) for c in middle_names):
            self._errors["middle_names"] = ErrorList()
            self._errors["middle_names"].append(error_messages["names"])

        #initials cleaner
        initials = self.cleaned_data.get("initials")
        if not initials.isalpha():
            self._errors["initials"] = ErrorList()
            self._errors["initials"].append(error_messages["initials"])

        #prefix cleaner
        prefix = self.cleaned_data.get("prefix")
        if any(str.isdigit(c) for c in prefix):
            self._errors["prefix"] = ErrorList()
            self._errors["prefix"].append(error_messages["names"])
        allowed_prefix = ["van", "van der", "der", "den", "van den", "van de", "de", "in het", "in 't", "di"]
        if prefix and prefix not in allowed_prefix:
            self._errors["prefix"] = ErrorList()
            self._errors["prefix"].append("Valid options: {0}".format(allowed_prefix))

        #place of birth cleaner
        place_of_birth = self.cleaned_data.get("place_of_birth")
        if any(str.isdigit(c) for c in place_of_birth):
            self._errors["place_of_birth"] = ErrorList()
            self._errors["place_of_birth"].append(error_messages["names"])

        #city cleaner
        city = self.cleaned_data.get("city")
        if any(str.isdigit(c) for c in city):
            self._errors["city"] = ErrorList()
            self._errors["city"].append(error_messages["names"])

        #home phone cleaner
        home_phone = self.cleaned_data.get("home_phone")
        if home_phone and not home_phone.isdigit():
           self._errors["home_phone"] = ErrorList()
           self._errors["home_phone"].append(error_messages["numbers"])

        mobile = self.cleaned_data.get("mobile")
        if mobile and not mobile.isdigit():
           self._errors["mobile"] = ErrorList()
           self._errors["mobile"].append(error_messages["numbers"])

    def save(self):
        # TODO: store in Alumnus
        academic_title = self.cleaned_data["academic_title"]
        initials       = self.cleaned_data["initials"]
        first_name     = self.cleaned_data["first_name"]
        middle_names   = self.cleaned_data["middle_names"]
        prefix         = self.cleaned_data["prefix"]
        gender         = self.cleaned_data["gender"]
        birth_date     = self.cleaned_data["birth_date"]
        nationality    = self.cleaned_data["nationality"]
        place_of_birth = self.cleaned_data["place_of_birth"]
        photo          = self.cleaned_data["photo"]
        biography      = self.cleaned_data["biography"]
        email          = self.cleaned_data["email"]
        home_phone     = self.cleaned_data["home_phone"]
        mobile         = self.cleaned_data["mobile"]
        homepage       = self.cleaned_data["homepage"]
        facebook       = self.cleaned_data["facebook"]
        twitter        = self.cleaned_data["twitter"]
        linkedin       = self.cleaned_data["linkedin"]
        city           = self.cleaned_data["city"]
        country        = self.cleaned_data["country"]

        msg = ""
        msg += "academic_title = {0}\n".format(academic_title)
        msg += "initials       = {0}\n".format(initials)
        msg += "first_name     = {0}\n".format(first_name)
        msg += "middle_names   = {0}\n".format(middle_names)
        msg += "prefix         = {0}\n".format(prefix)
        msg += "gender         = {0}\n".format(gender)
        msg += "birth_date     = {0}\n".format(birth_date)
        msg += "nationality    = {0}\n".format(nationality)
        msg += "place_of_birth = {0}\n".format(place_of_birth)
        msg += "photo          = {0}\n".format(photo)
        msg += "biography      = {0}\n".format(biography)
        msg += "email          = {0}\n".format(email)
        msg += "home_phone     = {0}\n".format(home_phone)
        msg += "mobile         = {0}\n".format(mobile)
        msg += "homepage       = {0}\n".format(homepage)
        msg += "facebook       = {0}\n".format(facebook)
        msg += "twitter        = {0}\n".format(twitter)
        msg += "linkedin       = {0}\n".format(linkedin)
        msg += "city           = {0}\n".format(city)
        msg += "country        = {0}\n".format(country)
        print(msg)


        variable_list = [academic_title, initials, first_name, middle_names,
        prefix, gender, birth_date, nationality, place_of_birth, photo, biography,
        email, home_phone, mobile, homepage, facebook, twitter, linkedin, city, country]

        for var in variable_list:
            print(var)
