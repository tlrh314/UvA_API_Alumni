from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
import os


@python_2_unicode_compatible
class ResearchTopic(models.Model):
    """Represents a research topic at API."""

    CATEGORY = (
        (1, 'Neutron stars and black holes'),
        (2, 'Cosmic explosions'),
        (3, 'Astroparticle physics'),
        (4, 'Planet formation and exoplanets'),
        (5, 'Stars, formation and evolution'),
    )

    topic = models.CharField(_('research topic'), unique=True, max_length=40)
    category = models.PositiveSmallIntegerField(
        _('category'), choices=CATEGORY, blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=500, unique=False)
    picture = models.ImageField(_('picture'), blank=True, null=True,
                                upload_to='uploads/images/research/topics/')
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('research topic')
        verbose_name_plural = _('research topics')
        ordering = ('topic', )

    def __str__(self):
        return str(self.topic)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(ResearchTopic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        cattypes = {1: 'compacts', 2: 'cosmics', 3: 'astroparticles',
                    4: 'planets', 5: 'stars'}
        return reverse('research:topic', kwargs={
            'category_type': cattypes[self.category],
            'pk': self.pk,
            'slug': self.slug})


@python_2_unicode_compatible
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
    title = models.CharField(max_length=160, default=_("Title Unknown"))
    date = models.DateField(help_text=_("Date of the thesis or defense"))
    type = models.CharField(max_length=3, choices=THESIS_TYPE, default='PhD')
    url = models.URLField(blank=True,
                          help_text=_("UvA DARE URL or other URL to thesis"))
    slug = models.SlugField(max_length=500, blank=False, unique=False)

    class Meta:
        verbose_name = _("thesis")
        verbose_name_plural = _("theses")

    def get_absolute_url(self):
        return reverse('research:thesis-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.author)
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(Thesis, self).save(*args, **kwargs)
