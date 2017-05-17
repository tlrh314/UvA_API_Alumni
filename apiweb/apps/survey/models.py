from __future__ import unicode_literals, absolute_import, division

import os
import os.path
from datetime import date

from django.db import models
# from django.db import IntegrityError
# from django.urls import reverse
# from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from django.template.defaultfilters import slugify
# from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible

# from jsonfield import JSONField
# from tinymce.models import HTMLField
# from django_countries.fields import CountryField


from ..alumni.models import Alumnus


class Sector(models.Model):
    name             = models.CharField(max_length=200)
    slug             = models.SlugField(unique=True, blank=True, null=True)

    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True)
    last_updated_by  = models.ForeignKey('auth.User', related_name="sector_updated",
        on_delete=models.SET_DEFAULT, default=270)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Job Sectors"


@python_2_unicode_compatible
class JobAfterLeaving(models.Model):
    """ Represents a job after leaving API """

    currently_occupating_job_choices = (
        (1, "Yes"),
        (2, "No"),
    )

    outside_inside_choices = (
        (1, "Yes"),
        (2, "No"),
    )

    location_job_choices = (
        (1, "NL"),
        (2, "Europe"),
        (3, "Great Bitain"),
        (4, "US"),
        (5, "Other"),
    )

    alumnus             = models.ForeignKey(Alumnus, related_name="job")
    position_name       = models.CharField(_("position name"), blank=True, max_length=40)
    current_job         = models.PositiveSmallIntegerField(_("current occupation"), choices=currently_occupating_job_choices, default=2)
    company_name        = models.CharField(_("company name"), blank=True, max_length=40)
    start_date          = models.DateField(_("date start job"), blank=True, null=True)
    stop_date           = models.DateField(_("date stop job"), blank=True, null=True)
    inside_academia     = models.PositiveSmallIntegerField(_("inside academia"), choices=outside_inside_choices, default=1)
    location_job        = models.PositiveSmallIntegerField(_("location job"), choices=location_job_choices, default=1)

    comments            = models.TextField(_("comments"), blank=True)
    last_updated_by     = models.ForeignKey('auth.User', related_name="jobs_updated",
        on_delete=models.SET_DEFAULT, default=270)
    date_created        = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated        = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    sector = models.ForeignKey(Sector, blank=True, null=True)



    class Meta:
        verbose_name = _("Job After Leaving API")
        verbose_name_plural = _("Jobs After Leaving API")

    def __str__(self):
        return self.alumnus.last_name