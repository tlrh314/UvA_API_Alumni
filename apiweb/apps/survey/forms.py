from datetime import datetime

from django import forms
from ..alumni.models import Alumnus

from .models import Sector
#from ..alumni.models import job_sectors


# TODO: put model info in the placeholder. 
class SurveyForm(forms.Form):
    this_year = datetime.now().year
    years_choices=range(1970, this_year)


    sector_choices = Sector.objects.all()
    print(sector_choices)

    location_job_choices = (
        (1, "NL"),
        (2, "Europe"),
        (3, "Great Bitain"),
        (4, "US"),
        (5, "Other"),
    )

    outside_inside_choices = (
        (1, "Yes"),
        (2, "No"),
    )

    currently_occupating_job_choices = (
        (1, "Yes"),
        (2, "No"),
    )

    current_job = forms.ChoiceField(
      required=True,
      choices=currently_occupating_job_choices,
      widget=forms.Select(
        attrs={"class": "form-control required"},
        )
    )

    start_date_job = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            years=years_choices,
        )
    )

    stop_date_job = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            years=years_choices,
            attrs={"class":"datePicker"}
        )
    )

    company_name = forms.CharField(
      required=False,
      max_length=100,
      widget=forms.TextInput(
       attrs={"placeholder": "What was the name of the company? no(t required)",
              "class": "form-control"}
       )
    )

    sector_job = forms.ModelChoiceField(
      required=True,
      queryset=Sector.objects.all(),
      widget=forms.Select(
        attrs={"class": "form-control required"},
        )
    )



    # sector_job = forms.ChoiceField(
    #   required=True,
    #   choices=sector_choices,
    #   widget=forms.Select(
    #     attrs={"class": "form-control required"},
    #     )
    # )

    location_job = forms.ChoiceField(
      required=True,
      choices=location_job_choices,
      widget=forms.Select(
        attrs={"class": "form-control required"},
        )
    )

    inside_academia = forms.ChoiceField(
      required=True,
      choices=outside_inside_choices,
      widget=forms.Select(
        attrs={"class": "form-control required"},
        )
    )

    comments = forms.CharField(
      required=False,
      max_length=100,
      widget=forms.Textarea(
       attrs={"placeholder": "",
              "class": "form-control"}
       )
    )



    #academic_job    = 
    #location_job    = 
    #comments        = 
    #company_name    = 
    #position_name   =
    #sector_job      =
    #type_of_job     = 

    # name = forms.CharField(max_length=100, widget=forms.TextInput(
    #    attrs={"class": "form-control required",
    #           "placeholder": "What is your name?"}))
    #message = forms.CharField(required=True, widget=forms.Textarea(
    #    attrs={"class": "form-control required",
    #           "placeholder": "What would you like to tell us?"}))
    #sender = forms.EmailField(required=False, widget=forms.EmailInput(
    #    attrs={"class": "form-control email",
    #           "placeholder": "email@adres.nl - so we know how to reach you"}))
    #cc_myself = forms.BooleanField(required=False, widget=forms.CheckboxInput(
    #    attrs={"class": "checkchoice"}))






    #First job info







# @python_2_unicode_compatible
# class JobAfterLeaving(models.Model):
#     """ Represents a job after leaving API """

#     currently_occupating_job_choices = (
#         (1, "Yes"),
#         (2, "No"),
#     )

#     outside_inside_choices = (
#         (1, "Yes"),
#         (2, "No"),
#     )

#     location_job_choices = (
#         (1, "NL"),
#         (2, "Europe"),
#         (3, "Great Bitain"),
#         (4, "US"),
#         (5, "Other"),
#     )

#     alumnus             = models.ForeignKey(Alumnus, related_name="job")
#     position_name       = models.CharField(_("position name"), blank=True, max_length=40)
#     current_job         = models.PositiveSmallIntegerField(_("current occupation"), choices=currently_occupating_job_choices, default=2)
#     company_name        = models.CharField(_("company name"), blank=True, max_length=40)
#     start_date          = models.DateField(_("date start job"), blank=True, null=True)
#     stop_date           = models.DateField(_("date stop job"), blank=True, null=True)
#     inside_academia     = models.PositiveSmallIntegerField(_("inside academia"), choices=outside_inside_choices, default=1)
#     location_job        = models.PositiveSmallIntegerField(_("location job"), choices=location_job_choices, default=1)

#     comments            = models.TextField(_("comments"), blank=True)
#     last_updated_by     = models.ForeignKey('auth.User', related_name="jobs_updated",
#         on_delete=models.SET_DEFAULT, default=270)
#     date_created        = models.DateTimeField(_("Date Created"), auto_now_add=True)
#     date_updated        = models.DateTimeField(_("Date Last Changed"), auto_now=True)

#     class Meta:
#         verbose_name = _("Job After Leaving API")
#         verbose_name_plural = _("Jobs After Leaving API")

#     def __str__(self):
#         return self.alumnus.last_name

