from __future__ import unicode_literals, absolute_import, division

import os
import os.path

from django.db import models
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible

from tinymce.models import HTMLField

from ..alumni.models import Alumnus

def get_thesis_pdf_location(instance, filename):
    """ the media directory is already included """
    return os.path.join("uploads", "theses", instance.type, filename)

def get_thesis_photo_location(instance, filename):
    """ the media directory is already included """
    return os.path.join("uploads", "theses", instance.type, filename)


@python_2_unicode_compatible
class Thesis(models.Model):
    """ Represents a thesis at API, either MSc or PhD. """

    THESIS_TYPE = (
        ("phd", "PhD"),
        ("msc", "Master of Science"),
        ("bsc", "Bachelor of Science"),
    )

    # Information about the thesis
    alumnus          = models.ForeignKey(Alumnus, related_name="theses", on_delete=models.CASCADE)
    type             = models.CharField(max_length=3, choices=THESIS_TYPE, default="PhD")
    date_start       = models.DateField(_("Starting date"), blank=True, null=True, help_text='Use format: YYYY-MM-DD')
    date_stop        = models.DateField(_("Date finished"), blank=True, null=True, help_text='Use format: YYYY-MM-DD')

    # Information about the thesis
    title     = models.CharField(_("Thesis Title"), blank=True, max_length=180)
    date_of_defence  = models.DateField(_("Defence date"), blank=True, null=True, help_text=_("Date of the thesis or defense. Use format: YYYY-MM-DD"))
    url       = models.URLField(blank=True, null=True, help_text=_("UvA DARE or other URL to thesis"))
    slug      = models.SlugField(blank=True, null=True, max_length=100, unique=True)
    advisor   = models.ManyToManyField(Alumnus, blank=True, related_name="students")
    dissertation_nr  = models.PositiveSmallIntegerField(_("PhD Dissertation Counter"), blank=True, null=True)
    # Slug is for url

    # TODO: set the maxlim for uploads to 30MB ?
    pdf       = models.FileField(_("Full Text (pdf)"),
        upload_to=get_thesis_pdf_location, blank=True, null=True)
    # abstract  = models.HTMLField(_("Abstract"), blank=True, null=True)
    photo     = models.ImageField(_("Thesis Photo"),
        upload_to=get_thesis_photo_location, blank=True, null=True)
    in_library= models.BooleanField(blank=True, default=False)

    comments         = models.TextField(_("comments"), blank=True)
    last_updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
        on_delete=models.SET_NULL, related_name="theses_updated")
    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True, help_text='Use format: YYYY-MM-DD')
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True, help_text='Use format: YYYY-MM-DD')

    # students supervised --> class? anders kan je er maar een paar invullen
    # privacy levels

    class Meta:
        verbose_name = _("MSc and/or PhD Thesis at API")
        verbose_name_plural = _("MSc and/or PhD Theses at API")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Get dissertation_nr and increment
        if self.type == "phd" and not self.dissertation_nr:
            dissertation_nr = 0
            for d in Thesis.objects.all():  # ugly bruteforce
                if d.dissertation_nr and d.dissertation_nr > dissertation_nr:
                    dissertation_nr = d.dissertation_nr
            self.dissertation_nr = dissertation_nr + 1

        # Set slug as firstname-lastname-thesistype with clash-prevention
        MAXCOUNT = 100
        count = 0
        base_slug = slugify(self.alumnus.full_name_no_title + "-" + self.type)
        self.slug = base_slug

        # The following loop should prevent a DB exception when
        # two people enter the same title at the same time
        while count < MAXCOUNT:
            try:
                super(Thesis, self).save(*args, **kwargs)
            except IntegrityError:
                count += 1
                self.slug = base_slug + "_{0}".format(count)
            else:
                break

    def get_absolute_url(self):
        return reverse("research:thesis-detail", args=[self.slug])

    @property
    def author(self):
        return self.alumnus.full_name
