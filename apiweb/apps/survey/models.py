from __future__ import unicode_literals, absolute_import, division

import os
import os.path
from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tinymce.models import HTMLField
from django_countries.fields import CountryField

from ..main.models import validate_only_one_instance
from ..alumni.models import Alumnus


@python_2_unicode_compatible
class SurveyText(models.Model):
    intro_message  = HTMLField(verbose_name=_("Survey Description"), blank=True)
    complete_message = HTMLField(verbose_name=_("Survey Complete Message"), blank=True)

    class Meta:
        verbose_name = _("Survey Explanation")
        verbose_name_plural = _("Survey Explanation")

    def clean(self):
        validate_only_one_instance(self)

    def __str__(self):
        return "SurveyText"


@python_2_unicode_compatible
class Sector(models.Model):
    name             = models.CharField(max_length=200)

    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True)
    last_updated_by  = models.ForeignKey('auth.User', related_name="sectors_updated",
        on_delete=models.SET_DEFAULT, default=270)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Job Sector"
        verbose_name_plural = "Job Sectors"


@python_2_unicode_compatible
class JobAfterLeaving(models.Model):
    """ Represents a job after leaving API """

    YES_OR_NO = (
        (1, "Yes"),
        (2, "No"),
    )

    JOB_LOCATION_CHOICES = (
        (1, "NL"),
        (2, "Europe"),
        (3, "Great Bitain"),
        (4, "US"),
        (5, "Other"),
    )

    alumnus             = models.ForeignKey(Alumnus, related_name="job")
    sector              = models.ForeignKey(Sector, blank=True, null=True)
    company_name        = models.CharField(_("Company Name"), blank=True, max_length=100)
    position_name       = models.CharField(_("Position Name"), blank=True, max_length=100)
    is_current_job      = models.PositiveSmallIntegerField(_("Is Current"), choices=YES_OR_NO, default=1)
    is_inside_academia  = models.PositiveSmallIntegerField(_("In Academia"), choices=YES_OR_NO, default=1)
    # location_job        = models.PositiveSmallIntegerField(_("location job"), choices=JOB_LOCATION_CHOICES, default=1)
    location_job        = CountryField(_("Location"), blank=True)
    start_date          = models.DateField(_("From"), blank=True, null=True)
    stop_date           = models.DateField(_("Until"), blank=True, null=True)

    comments            = models.TextField(_("comments"), blank=True)
    last_updated_by     = models.ForeignKey('auth.User', related_name="jobs_updated",
        on_delete=models.SET_DEFAULT, default=270)
    date_created        = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated        = models.DateTimeField(_("Date Last Changed"), auto_now=True)




    class Meta:
        verbose_name = _("Job After Leaving API")
        verbose_name_plural = _("Jobs After Leaving API")

    def __str__(self):
        return self.alumnus.last_name
