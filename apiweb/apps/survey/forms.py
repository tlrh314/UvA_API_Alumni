import logging
import sys
from datetime import datetime

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import widgets
from django.forms.utils import ErrorList
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django_countries import countries
from tinymce.widgets import TinyMCE

from ..alumni.models import AcademicTitle, Alumnus
from .models import JobAfterLeaving, Sector

error_messages = {
    "names": "Names cannot contain numbers",
    "numbers": "Phonenumbers can only contain numbers",
    "initials": "Initials can only contain letters",
    "duplicate_email": "This email adress is already in use!",
}

TINYMCE_LOCAL_CONFIG = {
    "selector": "textarea",
    "height": 200,
    "width": 0,
    "menubar": False,
    "statusbar": False,
    "elementpath": False,
    "plugins": ["paste"],
    "toolbar1": "undo redo | bold italic | bullist numlist outdent indent | ",
    "toolbar2": "",
    "paste_as_text": True,
}


class SendSurveyForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    # Here we overwrite the save method because the PasswordResetForm gets
    # all users given an e-mail address, but we want to e-mail one specific
    # alumnus only once. This avoids sending the same mail multiple times.
    # Also, here we set the templates to use for the subject and e-mail.
    # Based on Django 1.11, if Django is upgraded: check changes to PasswordResetForm

    def save(
        self,
        alumnus,
        domain_override=None,
        subject_template_name="survey/survey_email_subject.txt",
        email_template_name="survey/send_survey_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """

        logger = logging.getLogger("survey")
        logger.debug("Running save() method of SendSurveyForm")

        email = self.cleaned_data["email"]
        logger.info("Sending Survey Email to: {0}".format(email))
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
            "uid": urlsafe_base64_encode(force_bytes(alumnus.pk)),
            "user": alumnus,
            "token": token_generator.make_token(alumnus),
            "protocol": "https" if use_https else "http",
        }

        if extra_email_context is not None:
            context.update(extra_email_context)

        # Small hack to easily test the email sending on the development server.
        if "runserver" in sys.argv:
            survey_link = "http://127.0.0.1:8000/survey/{0}/{1}".format(
                context["uid"], context["token"]
            )
            print("\t%s" % (survey_link))
            logger.info("Mail was not sent because 'runserver' in sys.argv")
        else:
            logger.info("Mail was sent to: {0}".format(email))
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                email,
                html_email_template_name=html_email_template_name,
            )

    # Here we overwrite the send_mail method because we want to bcc all the
    # survey emails that we send out to survey@api-alumni.nl
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
        bcc_email="survey@api-alumni.nl",
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """

        logger = logging.getLogger("survey")
        logger.debug("Running send_mail() method of SendSurveyForm")

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email], bcc=[bcc_email]
        )
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        logger.info("Sending a copy to: {0}".format(bcc_email))
        email_message.send()


class SurveyCareerInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyCareerInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JobAfterLeaving
        exclude = (
            "alumnus",
            "date_created",
            "date_updated",
            "last_updated_by",
            "which_position",
        )

    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    years_choices = range(1900, datetime.now().year + 10)[::-1]

    sector = forms.ModelChoiceField(
        required=False,
        queryset=Sector.objects.all().order_by("name"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    company_name = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    position_name = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    is_inside_academia = forms.ChoiceField(
        required=False,
        choices=JobAfterLeaving.YES_OR_NO,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    is_inside_astronomy = forms.ChoiceField(
        required=False,
        choices=JobAfterLeaving.YES_OR_NO,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    location_job = forms.ChoiceField(
        required=False,
        choices=BLANK_CHOICE_DASH + list(countries),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    start_date = forms.DateField(
        required=False,
        widget=widgets.SelectDateWidget(
            years=years_choices, attrs={"class": "datetime-input"}
        ),
    )

    stop_date = forms.DateField(
        required=False,
        widget=widgets.SelectDateWidget(years=years_choices, attrs={"class": ""}),
    )

    comments = forms.CharField(
        required=False, widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG)
    )

    show_job = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

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
        exclude = (
            "user",
            "show_person",
            "passed_away",
            "nickname",
            "student_id",
            "mugshot",
            "slug",
            "last_checked",
            "position",
            "specification",
            "office",
            "work_phone",
            "ads_name",
            "research",
            "contact",
            "comments",
            "date_created",
            "date_updated",
            "last_updated_by",
            "zipcode",
            "streetname",
            "streetnumber",
            "address",
            # Below has to be removed b/c Alumnus is an extension of AbstractBaseUser
            "password",
            "last_login",
            "is_superuser",
            "groups",
            "user_permissions",
            "username",
            "is_staff",
            "is_active",
            "date_joined",
            "survey_info_updated",
            "survey_email_sent",
        )

    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    years_choices = range(1900, datetime.now().year + 1)[::-1]

    academic_title = forms.ModelChoiceField(
        required=False,
        queryset=AcademicTitle.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    initials = forms.CharField(
        required=False,
        help_text="Please use letters only, no dots",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    first_name = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    middle_names = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    prefix = forms.CharField(
        required=False,
        help_text="Tussenvoegsel, e.g. 'van der', 'de'",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    last_name = forms.CharField(
        max_length=128, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    gender = forms.ChoiceField(
        required=False,
        choices=Alumnus.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    birth_date = forms.DateField(
        required=False,
        widget=widgets.SelectDateWidget(years=years_choices, attrs={"class": ""}),
    )

    nationality = forms.ChoiceField(
        required=False,
        choices=BLANK_CHOICE_DASH + list(countries),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    place_of_birth = forms.CharField(
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    mugshot = forms.ImageField(required=False)

    biography = forms.CharField(
        required=False, max_length=2048, widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG)
    )

    show_biography = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        required=False,
        help_text="Your email address will also serve as a way to log in",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    show_email = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

    home_phone = forms.CharField(
        required=False,
        help_text="Please use digits only. This information will not be publicly displayed",
        max_length=24,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    mobile = forms.CharField(
        required=False,
        help_text="Please use digits only. This information will not be publicly displayed",
        max_length=24,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    homepage = forms.URLField(
        required=False,
        help_text="Please give the full URL to your homepage",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    show_homepage = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

    facebook = forms.URLField(
        required=False,
        help_text="Please give the full URL to your Facebook",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    show_facebook = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

    twitter = forms.URLField(
        required=False,
        help_text="Please give the full URL to your Twitter",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    show_twitter = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

    linkedin = forms.URLField(
        required=False,
        help_text="Please give the full URL to LinkedIn",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    show_linkedin = forms.BooleanField(
        required=False,
        help_text="Choose whether to display this information on your profile page",
        widget=forms.Select(choices=BOOL_CHOICES, attrs={"class": "form-control"}),
    )

    city = forms.CharField(
        required=False,
        max_length=24,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    country = forms.ChoiceField(
        required=False,
        choices=BLANK_CHOICE_DASH + list(countries),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    field_order = [
        "academic_title",
        "initials",
        "first_name",
        "middle_names",
        "prefix",
        "last_name",
        "gender",
        "birth_date",
        "nationality",
        "place_of_birth",
        "mugshot",
        "biography",
        "show_biography",
        "email",
        "show_email",
        "home_phone",
        "mobile",
        "homepage",
        "show_homepage",
        "facebook",
        "show_facebook",
        "twitter",
        "show_twitter",
        "linkedin",
        "show_linkedin",
        "city",
        "country",
    ]

    def clean(self):
        super().clean()
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

        # Because there is also a possibility to log in with email, one must not use an
        # email which is already in use.
        # TODO: if the user has an email, but the form is empty, that means that the
        # person wants to remove the data, but this way wouldt let it
        # SO make a check whether there is instance data but form data is empty
        email = self.cleaned_data.get("email")
        # Remove this instance object from duplicate emails object list
        if email:
            duplicate_emails_excluded = Alumnus.objects.filter(email=email).exclude(
                pk=self.instance.pk
            )
            if len(duplicate_emails_excluded) > 0:
                self.errors["email"] = ErrorList()
                self.errors["email"].append(error_messages["duplicate_email"])
