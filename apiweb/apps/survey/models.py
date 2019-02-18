from __future__ import unicode_literals, absolute_import, division

import os
import os.path
from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tinymce.models import HTMLField
from django_countries.fields import CountryField

from ..main.models import validate_only_one_instance
from ..alumni.models import Alumnus


@python_2_unicode_compatible
class Sector(models.Model):
    name             = models.CharField(max_length=200)

    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True)
    last_updated_by  = models.ForeignKey(get_user_model(), null=True,
        on_delete=models.SET_NULL, related_name="sectors_updated")

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

    WHICH_POSITION_CHOICES = (
        (0, "Current"),
        (1, "First"),
        (2, "Second"),
        (3, "Third"),
    )


    alumnus             = models.ForeignKey(Alumnus, related_name="job", on_delete=models.CASCADE)
    sector              = models.ForeignKey(Sector, blank=True, null=True, on_delete=models.SET_NULL)
    company_name        = models.CharField(_("Company Name"), blank=True, max_length=100)
    position_name       = models.CharField(_("Position Name"), blank=True, max_length=100)
    is_inside_academia  = models.PositiveSmallIntegerField(_("In Academia"), choices=YES_OR_NO, default=1)
    is_inside_astronomy = models.PositiveSmallIntegerField(_("In Astronomy"), choices=YES_OR_NO, null=True, blank=True)

    location_job        = CountryField(_("Location"), blank=True)
    start_date          = models.DateField(_("From"), blank=True, null=True)
    stop_date           = models.DateField(_("Until"), blank=True, null=True)

    #Have 4 options for this, current, first after, second after, third after
    which_position      = models.PositiveSmallIntegerField(_("Which position"), choices=WHICH_POSITION_CHOICES, default=0)

    comments            = models.TextField(_("comments"), blank=True)
    last_updated_by     = models.ForeignKey(get_user_model(), null=True,
        on_delete=models.SET_NULL, related_name="jobs_updated")
    date_created        = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated        = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    # Privacy
    show_job = models.BooleanField(_("Show job on personal page"), blank=True, default=True)

    class Meta:
        verbose_name = _("Job After Leaving API")
        verbose_name_plural = _("Jobs After Leaving API")

    def __str__(self):
        return self.alumnus.last_name
