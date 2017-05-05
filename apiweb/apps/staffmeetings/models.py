from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import os
import os.path



def get_private_location(instance, filename):
    fname, _, extension = filename.rpartition('.')
    slug = '{}.{}'.format(slugify(fname), extension)
    return os.path.join("uploads", "staff_meetings",
                        instance.date.strftime("%Y-%m-%d"), "private", slug)


def get_public_location(instance, filename):
    fname, _, extension = filename.rpartition('.')
    slug = '{}.{}'.format(slugify(fname), extension)
    return os.path.join("uploads", "staff_meetings",
                        instance.date.strftime("%Y-%m-%d"), "public", slug)



class Staffmeeting(models.Model):
    """Represents a staffmeeting at API."""

    date = models.DateField(_('date staff meeting'), unique=True)

    agenda = models.FileField(_('agenda'),
                              upload_to=get_private_location,
                              blank=True, null=True)
    report = models.FileField(_('report'),
                              upload_to=get_private_location,
                              blank=True, null=True)
    appendix_1 = models.FileField(_('appendix_1'),
                                  upload_to=get_private_location,
                                  blank=True, null=True)
    appendix_2 = models.FileField(_('appendix_2'),
                                  upload_to=get_private_location,
                                  blank=True, null=True)
    appendix_3 = models.FileField(_('appendix_3'),
                                  upload_to=get_private_location,
                                  blank=True, null=True)
    decisions = models.FileField(_('decisions'),
                                 upload_to=get_public_location,
                                 blank=True, null=True)
    appendix_A = models.FileField(_('appendix_A'),
                                  upload_to=get_public_location,
                                  blank=True, null=True)
    appendix_B = models.FileField(_('appendix_B'),
                                  upload_to=get_public_location,
                                  blank=True, null=True)


    class Meta:
        verbose_name = _('staff meeting')
        verbose_name_plural = _('staff meetings')
        ordering = ('-date', )
