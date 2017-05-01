from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db import models
from datetime import datetime
from itertools import islice, chain
import re


def clean_text(text):
    """Remove style attributes from tags

    Removes style attributes from HTML tags; also removes
    all <span.*> and </span> attributes.

    This should make life a lot easier when copy-pasting into a text
    field that is augmented by tiny_mce: the layout of the pasted text
    should conform much better to the overall layout after removal of
    the span tag.

    """

    # remove <span> tags
    text = re.sub(r'</?span[^>]*>', '', text)
    # remove style attributes inside other tags
    text = re.sub(r'(?P<tagstart><[^>]+?)style="[^"]*"', '\g<tagstart>', text)
    return text


class JobManager(models.Manager):

    def current(self):
        now = datetime.now().date()
        queryset = super(JobManager, self).get_queryset().filter(
            visible=True).filter(
                date_on__lte=now).filter(date_off__gte=now)
        q1 = list(queryset.filter(deadline__gte=now).order_by('deadline'))
        q2 = list(queryset.filter(deadline__lt=now).order_by('-deadline'))
        return q1+q2


class Job(models.Model):
    title = models.CharField(max_length=160, default="",
                             help_text=_("eg: PhD vacancy in gamma-ray bursts "
                                         "research"))
    teaser = models.TextField(help_text=_("One or two sentences for front "
                                          "page, below the title"))
    text = models.TextField(help_text=_("Main advertising text"))
    deadline = models.DateField(help_text=_("Application deadline"))
    contact = models.CharField(max_length=300, help_text=_(
        "Contact person, phone, email etc"))
    website = models.CharField(max_length=160, help_text=_(
        "Website with more information (eg about the research, group etc)"),
                               blank=True)
    date_on = models.DateField(help_text=_("date from which the item is "
                                           "visible on the site (inclusive)"))
    date_off = models.DateField(help_text=_("date until which the item is "
                                            "visible on the site (inclusive)"))
    visible = models.BooleanField(_('visible on site'), default=True,
                                  help_text=_(
                                      "Explicitly turn visibility for an item "
                                      "on or off. When visibility is turned "
                                      "on, behaviour follows the on/off dates"))
    slug = models.SlugField(max_length=200, blank=True, unique=False)

    # We've added a method to JobManager, but not overridden any old method
    # So, we can safely assign JobManager to objects (the default manager)
    objects = JobManager()

    def save(self, *args, **kwargs):
        self.text = clean_text(self.text)
        self.slug = slugify(self.title)
        super(Job, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('jobs:detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})
