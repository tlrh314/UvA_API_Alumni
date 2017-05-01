from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta


class ProjectManager(models.Manager):
    def current(self, year=None):
        now = datetime.now()
        projects = super(ProjectManager, self).get_queryset().filter(
            visible=True).filter(date_on__lte=now).filter(
                date_off__gte=now)
        if isinstance(year, (list, set, tuple)):
            projects = projects.filter(year__in=year)
        elif isinstance(year, int):
            projects = projects.filter(year=year)
        return projects


@python_2_unicode_compatible
class Project(models.Model):
    title = models.CharField(max_length=160, default="",
                             help_text=_("Title for project"))
    text = models.TextField(help_text=_("Main text"))
    contact = models.CharField(max_length=300, help_text=_(
        "Contact person, phone, email etc"))
    academic_year = models.PositiveIntegerField(
        help_text="Starting calendar year (eg, '2008' for 2008-2009)")
    date_on = models.DateField(help_text=_("date from which the item is "
                                           "visible on the site (inclusive)"))
    date_off = models.DateField(help_text=_("date until which the item is "
                                            "visible on the site (inclusive)"))
    visible = models.BooleanField(_('visible on site'), default=True,
                                  help_text=_(
                                      "Explicitly turn visibility for an item "
                                      "on or off. When visibility "
                                      "is turned on, behaviour follows the "
                                      "on/off dates"))
    slug = models.SlugField(max_length=500, unique=False)

    # We've added a method to ProjectManager, but not overridden any
    # old method. Thus, we can safely assign ProjectManager to objects
    # (the default manager)
    objects = ProjectManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class BachelorProject(Project):
    YEAR_CHOICES = (
        (1, _('first')),
        (2, _('second')),
        (3, _('third')),
        )
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=3)

    def get_absolute_url(self):
        return reverse('education:bachelor-projects-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        verbose_name = "Bachelor project"

    def __str__(self):
        return super(BachelorProject, self).__str__()


@python_2_unicode_compatible
class MasterProject(Project):
    YEAR_CHOICES = (
        (4, _('fourth')),
        (5, _('fifth')),
        )
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=5)

    def get_absolute_url(self):
        return reverse('education:master-projects-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        verbose_name = "Master project"

    def __str__(self):
        return super(MasterProject, self).__str__()


@python_2_unicode_compatible
class CourseTopic(models.Model):
    SEMESTER_CHOICES = (
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV"),
        (5, "V"),
        (6, "VI"),
        )
    name = models.CharField(max_length=80, default="",
                            help_text=_("Name of class to be taught"))
    teacher = models.CharField(max_length=80, default="",
                               help_text=_("  "))
    description = models.TextField(blank=True)
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES,
                                                default=1, help_text=_("  "))
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CourseTopic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('education:course-topic-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.name
