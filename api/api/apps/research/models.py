from __future__ import unicode_literals, absolute_import, division

import os

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink
from django.core.exceptions import ObjectDoesNotExist

from tinymce.models import HTMLField


class ResearchTopic(models.Model):
    """Represents a research topic at API."""

    CATEGORY = (
        (0, 'None'),
        (1, 'Neutron stars and black holes'),
        (2, 'Cosmic explosions'),
        (3, 'Astroparticle physics'),
        (4, 'Planet formation and exoplanets'),
        (5, 'Stars, formation and evolution'),
    )

    topic    = models.CharField(_('research topic'), unique=True, max_length=40)
    category = models.PositiveSmallIntegerField(_('category'), choices=CATEGORY)
    slug     = models.SlugField(_('slug'), unique=True)
    picture  = models.ImageField(_('picture'), blank=True, null=True,
                                 upload_to='uploads/images/research/topics/')
    description = HTMLField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('research topic')
        verbose_name_plural = _('research topics')
        ordering = ('topic', )

    def __unicode__(self):
        return u'%s' % self.topic

    def save(self, *args, **kwargs):
        MAXCOUNT = 100
        count = 0
        base_slug = slugify(self.topic)
        self.slug = base_slug
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        # The following loop should prevent a DB exception when
        # two people enter the same title at the same time
        while count < MAXCOUNT:
            try:
                super(ResearchTopic, self).save(*args, **kwargs)
            except IntegrityError:
                count += 1
                self.slug = base_slug + "_%d" % count
            else:
                break

    @permalink
    def get_absolute_url(self):
        cattypes = {0: 'none', 1: 'compacts', 2: 'cosmics', 3: 'astroparticles', 4: 'planets', 5: 'stars'}
        return ('research:topic', None,
               {'category_type': cattypes[self.category],
                'slug': self.slug})


class Thesis(models.Model):
    """Represents a thesis at API."""

    THESIS_TYPE = (
        ('phd', 'PhD'),
        ('msc', 'Master'),
        ('bsc', 'Bachelor'),
    )

    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Unknown'),
    )

    author = models.CharField(max_length=80)
    gender = models.PositiveSmallIntegerField(
             _('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    title  = models.CharField(max_length=160, default=_("Title Unknown"))
    date   = models.DateField(help_text=_("Date of the thesis or defense"))
    type   = models.CharField(max_length=3, choices=THESIS_TYPE, default='PhD')
    url    = models.URLField(blank=True, help_text=_("UvA DARE URL or other URL to thesis"))
    slug   = models.SlugField(max_length=100, blank=False, unique=True)

    class Meta:
        verbose_name = _("thesis")
        verbose_name_plural = _("theses")

    @models.permalink
    def get_absolute_url(self):
        return ('research:thesis-detail', [self.slug], {})

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        MAXCOUNT = 100
        count = 0
        base_slug = slugify(self.author)
        self.slug = base_slug
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        # The following loop should prevent a DB exception when
        # two people enter the same author at the same time
        while count < MAXCOUNT:
            try:
                super(Thesis, self).save(*args, **kwargs)
            except IntegrityError:
                count += 1
                self.slug = base_slug + "_%d" % count
            else:
                break


