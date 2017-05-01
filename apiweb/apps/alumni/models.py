from __future__ import unicode_literals, absolute_import, division

import os
import os.path
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models import permalink
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible

# from tinymce.models import HTMLField

from ..research.models import ResearchTopic


def get_mugshot_location(instance, filename):
    return os.path.join("uploads", "images", "people", "mugshots",
                        instance.user.username, filename)

def get_photo_location(instance, filename):
    return os.path.join("uploads", "images", "people", "photos",
                        instance.user.username, filename)

def get_thesis_location(instance, filename):
    return os.path.join("uploads","documents","people","thesis",
            instance.user.username,filename)


@python_2_unicode_compatible
class Alumnus(models.Model):
    """ Represents an alumnus of API. """

    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Unknown'),
    )

    POSITION = {
        'DIRECTOR': 1,
        'STAFF': 2,
        'NOVA': 3,
        'ADJUNCT': 4,
        'POSTDOC': 5,
        'PHD': 6,
        'EMERITUS': 7,
        'GUEST': 8,
        'MASTER': 9,
        'BACHELOR': 10,
        'DEVELOPER': 11}

    POSITION_OPTIONS = (
        (POSITION['DIRECTOR'], _("Director")),
        (POSITION['STAFF'], _("Faculty Staff")),
        (POSITION['NOVA'], _("Nova")),
        (POSITION['ADJUNCT'], _("Adjunct Staff")),
        (POSITION['POSTDOC'], _("Postdoc")),
        (POSITION['PHD'], _("PhD Student")),
        (POSITION['EMERITUS'], _("Emeritus")),
        (POSITION['GUEST'], _("Guest")),
        (POSITION['MASTER'], _("Master Student")),
        (POSITION['BACHELOR'], _("Bachelor Student")),
        (POSITION['DEVELOPER'], _("Software Developer")),
    )

    # Account information
    user            = models.OneToOneField(User, unique=True, related_name='alumnus')
    show_person     = models.BooleanField(_('alumnus visible on website'), default=True)

    # Personal information
    first_name      = models.CharField(_('first name'), blank=True, max_length=40)
    prefix          = models.CharField(_('prefix'), blank=True, max_length=40)
    last_name       = models.CharField(_('last name'), max_length=40)
    title           = models.CharField(_('title'), blank=True, max_length=40)
    initials        = models.CharField(_('initials'), blank=True, max_length=40)
    gender          = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date      = models.DateField(_('birth date'), blank=True, null=True)
    nationality     = models.CharField(_('nationality'), blank=True, max_length=40)
    place_of_birth  = models.CharField(_('place of birth'), blank=True, max_length=40)
    mugshot         = models.ImageField(_('mugshot'), upload_to=get_mugshot_location, blank=True, null=True)
    photo           = models.ImageField(_('photo'), upload_to=get_photo_location, blank=True, null=True)
    # biography       = HTMLField(_('biography'), blank=True)
    biography       = models.TextField(_('biography'), blank=True)
    slug            = models.SlugField(_('slug'), unique=True)

    # Contact information
    linkedin        = models.URLField(_('linkedin'), blank=True, null=True)
    facebook        = models.URLField(_('facebook'), blank=True, null=True)
    email           = models.EmailField(_('email'), blank=True, null=True)
    home_phone      = models.CharField(_('home telephone'), blank=True, max_length=40)
    mobile          = models.CharField(_('mobile'), blank=True, max_length=40)
    homepage        = models.URLField(_('homepage'), blank=True, null=True)

    # Address information
    address         = models.CharField(_('address'), blank=True, max_length=40)
    streetname      = models.CharField(_('streetname'),blank = True, max_length=40)
    streetnumber    = models.CharField(_('streetnumber'),blank = True, max_length=40)
    zipcode         = models.CharField(_('zipcode'), blank=True, max_length=40)
    city            = models.CharField(_('city'), blank=True, max_length=40)
    country         = models.CharField(_('country'), blank=True, max_length=40)

    # Science information
    position        = models.PositiveSmallIntegerField(_('position'), choices=POSITION_OPTIONS, default=5)
    office          = models.CharField(_('office'), blank=True, max_length=40)
    work_phone      = models.CharField(_('work telephone'), blank=True, max_length=40)
    ads_name        = models.CharField(_('ads name'), blank=True, max_length=40)
    research        = models.ManyToManyField(ResearchTopic, verbose_name=_("research"), blank=True, related_name='alumnus_interest')
    contact         = models.ManyToManyField(ResearchTopic, verbose_name=_("contact"), blank=True, related_name='alumnus_contact')

    #Extra information
    comments        = models.TextField(_('comments'), blank=True)

    class Meta:
        verbose_name = _('alumnus')
        verbose_name_plural = _('alumni')
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        try:
            # Work around a nasty bug in Django: don't use user=self.user
            # Also: is user__username better than user__pk?
            Alumnus.objects.exclude(
                user__username=self.user.username).get(slug=self.slug)
        except ObjectDoesNotExist:
            pass
        else:
            count = Alumnus.objects.filter(slug__contains = self.slug).count()
            self.slug = '%s_%s' % (self.slug, str(count + 1))
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(Alumnus, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('alumnus:alumnus-detail', None, {'slug': self.slug})

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return ('{} {} {}'.format(
            self.first_name, self.prefix, self.last_name)).replace("  ", " ")

    @property
    def age(self):
        TODAY = date.today()
        return '{}'.format(int((TODAY-self.birth_date).days/365.0))


@python_2_unicode_compatible
class Job(models.Model):
    """ Represents a job after leaving API """

    currently_occupating_job_choices = (
        (1,'Yes'),
        (2,'No'),
    )

    outside_inside_choices = (
        (1, 'Yes'),
        (2, 'No'),
    )

    location_job_choices = (
        (1, 'NL'),
        (2, 'Europe'),
        (3, 'Great Bitain'),
        (4, 'US'),
        (5, 'Other'),
    )

    alumnus             = models.ForeignKey(Alumnus, related_name="jobs")
    position_name       = models.CharField(_('position name'), blank=True,max_length=40)
    current_job         = models.PositiveSmallIntegerField(_('current occupation'), choices=currently_occupating_job_choices, default=2)
    company_name        = models.CharField(_('company name'), blank=True, max_length=40)
    start_date          = models.DateField(_('date start job'), blank=True, null=True)
    stop_date           = models.DateField(_('date start job'), blank=True, null=True)
    inside_academia     = models.PositiveSmallIntegerField(_('inside academia'), choices=outside_inside_choices, default=1)
    location_job        = models.PositiveSmallIntegerField(_('location job'), choices=location_job_choices, default=1)


@python_2_unicode_compatible
class MastersDegree(models.Model):
    #Masters information @api
    alumnus             = models.ForeignKey(Alumnus, related_name="masters")
    date_start_master   = models.DateField(_('date start master'), blank=True, null=True)
    date_stop_master    = models.DateField(_('date stop master'), blank=True, null=True)
    #thesis_file =


    #Thesis topic/name/link
    #supervisor(s)
    #privacy levels


@python_2_unicode_compatible
class PhdDegree(models.Model):
    alumnus          = models.ForeignKey(Alumnus, related_name="phd")
    date_start_phd   = models.DateField(_('date start phd'), blank=True, null=True)
    date_stop_phd    = models.DateField(_('date stop phd'), blank=True, null=True)
    phd_defence_date = models.DateField(_('phd defence date'), blank=True, null=True)
    #thesis_file      = models.


    #thesis topic/name/link/field
    #supervisors
    #students supervised --> class? anders kan je er maar een paar invullen
    #privacy levels


@python_2_unicode_compatible
class PostdocPosition(models.Model):
    #postdoc information @api
    alumnus             = models.ForeignKey(Alumnus, related_name="postdoc")
    date_start_postdoc  = models.DateField(_('date start postdoc'), blank=True, null=True)
    date_stop_postdoc   = models.DateField(_('date stop postdoc'), blank=True, null=True)
    #supervisors,
    #field,

    #privacy levels


@python_2_unicode_compatible
class Thesis(models.Model):
    """ Represents a thesis at API. """

    # THESIS_TYPE = (
    #     ('phd', 'PhD'),
    #     ('msc', 'Master'),
    #     ('bsc', 'Bachelor'),
    # )

    #author = models.ForeignKey(Alumnus, related_name="thesis")
    title  = models.CharField(max_length=160, default=_("Title Unknown"))
    date   = models.DateField(help_text=_("Date of the thesis or defense"))
    url    = models.URLField(blank=True, help_text=_("UvA DARE URL or other URL to thesis"))
    slug   = models.SlugField(max_length=100, blank=False, unique=True)
    supervisor = models.ManyToManyField(Alumnus, related_name='supervisor')

    #Degree = models.ForeignKey(MastersDegree if self.type == 'msc' else PhdDegree,)
    #phd =

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
        base_slug = slugify(self.topic)
        self.slug = base_slug
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


class MasterThesis(Thesis):
    degree = models.OneToOneField(MastersDegree)

    @property
    def type():
        return "MSc"

    @property
    def author(self):
        return self.degree.alumnus.full_name


class PhdThesis(Thesis):
    degree = models.OneToOneField(PhdDegree)

    @property
    def type():
        return "PhD"

    @property
    def author(self):
        return self.degree.alumnus.full_name
