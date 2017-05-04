from __future__ import unicode_literals, absolute_import, division

import os
import os.path
from datetime import date

from django.db import models
from django.db import IntegrityError
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models import permalink
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible

from tinymce.models import HTMLField

from ..research.models import ResearchTopic


def get_mugshot_location(instance, filename):
    return os.path.join("uploads", "images", "people", "mugshots",
                        instance.user.username, filename)

def get_photo_location(instance, filename):
    return os.path.join("uploads", "images", "people", "photos",
                        instance.user.username, filename)

def get_thesis_location(instance, filename):
    return os.path.join("uploads", "documents", "people", "thesis",
            instance.user.username, filename)


@python_2_unicode_compatible
class CurrentPosition(models.Model):
    name = models.CharField(max_length=80, help_text=_(
        "Name of position (e.g., director, faculty staff, postdoc, "
        "PhD student, ...)"))
    plural = models.CharField(max_length=80, blank=True, help_text=_(
        "Full plural name, if this is not a simple appended 's'"))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("people:position-list", kwargs={"position": self.name})


@python_2_unicode_compatible
class Alumnus(models.Model):
    """ Represents an alumnus of API. """

    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
        (3, "Unknown"),
    )

    # Account information
    user            = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name="alumnus")
    show_person     = models.BooleanField(_("alumnus visible on website"), default=True)

    # Personal information
    title           = models.CharField(_("title"), blank=True, max_length=40)
    initials        = models.CharField(_("initials"), blank=True, max_length=40)
    first_name      = models.CharField(_("first name"), blank=True, max_length=40)
    nickname        = models.CharField(_("nickname"), blank=True, max_length=40)
    middle_names    = models.CharField(_("middle names"), blank=True, max_length=120)
    prefix          = models.CharField(_("prefix"), blank=True, max_length=40)
    last_name       = models.CharField(_("last name"), max_length=40)
    gender          = models.PositiveSmallIntegerField(_("gender"), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date      = models.DateField(_("birth date"), blank=True, null=True)
    nationality     = models.CharField(_("nationality"), blank=True, max_length=40)
    place_of_birth  = models.CharField(_("place of birth"), blank=True, max_length=40)
    student_id      = models.CharField(_("student_id"), blank=True, max_length=10)
    mugshot         = models.ImageField(_("mugshot"), upload_to=get_mugshot_location, blank=True, null=True)
    photo           = models.ImageField(_("photo"), upload_to=get_photo_location, blank=True, null=True)
    biography       = HTMLField(_("biography"), blank=True, default="")
    slug            = models.SlugField(_("slug"), unique=True)

    # Contact information
    email           = models.EmailField(_("email"), blank=True, null=True)
    home_phone      = models.CharField(_("home telephone"), blank=True, max_length=40)
    mobile          = models.CharField(_("mobile"), blank=True, max_length=40)
    homepage        = models.URLField(_("homepage"), blank=True, null=True)
    facebook        = models.URLField(_("facebook"), blank=True, null=True)
    twitter         = models.URLField(_("twitter"), blank=True, null=True)
    linkedin        = models.URLField(_("linkedin"), blank=True, null=True)

    # Address information
    address         = models.CharField(_("address"), blank=True, max_length=40)
    streetname      = models.CharField(_("streetname"),blank=True, max_length=40)
    streetnumber    = models.CharField(_("streetnumber"),blank=True, max_length=40)
    zipcode         = models.CharField(_("zipcode"), blank=True, max_length=40)
    city            = models.CharField(_("city"), blank=True, max_length=40)
    country         = models.CharField(_("country"), blank=True, max_length=40)

    # Current position at API
    current_position= models.ManyToManyField(CurrentPosition, blank=True)
    specification   = models.CharField(max_length=255, blank=True,
        help_text=_("Type of grant, or other indicator of funding"))
    office          = models.CharField(_("office"), blank=True, max_length=40)
    work_phone      = models.CharField(_("work telephone"), blank=True, max_length=40)
    ads_name        = models.CharField(_("ads name"), blank=True, max_length=40)
    research        = models.ManyToManyField(ResearchTopic, verbose_name=_("research"),
        blank=True, related_name="alumnus_research")
    contact         = models.ManyToManyField(ResearchTopic, verbose_name=_("contact"),
        blank=True, related_name="alumnus_contact")

    # Extra information
    comments        = models.TextField(_("comments"), blank=True)

    class Meta:
        verbose_name = _("Alumnus")
        verbose_name_plural = _("Alumni")
        ordering = ("last_name", "first_name")

    def __str__(self):
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
            self.slug = "{0}_{1}".format(self.slug, str(count + 1))
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(Alumnus, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ("alumnus:alumnus-detail", None, {"slug": self.slug})

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return ("{} {} {}".format(
            self.first_name, self.prefix, self.last_name)).replace("  ", " ")

    @property
    def age(self):
        TODAY = date.today()
        return "{}".format(int((TODAY-self.birth_date).days/365.0))


@receiver(signals.post_delete, sender=Alumnus)
def delete_user(sender, instance=None, **kwargs):
    """ When Alumnus instance is deleted, the post_delete signal is sent.
        Here we receive the post_delete signal to also remove the related
        User instance. Note that this does not ask for confirmation in
        the Admin upon deleting the Alumnus instance. """
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()


# class StudentSupervisorRelationship(models.Model):
#     student = models.ForeignKey('Alumnus', related_name='student')
#     supervisor = models.ForeignKey('Alumnus', related_name='supervisor')
#
#     class Meta:
#         unique_together = ('student', 'supervisor')


@python_2_unicode_compatible
class Degree(models.Model):
    """ Represents a degree at API, either MSc or PhD.
        A degree is obtained by writing and defending a thesis. """

    DEGREE_TYPE = (
        ("phd", "PhD"),
        ("msc", "Master of Science"),
        ("bsc", "Bachelor of Science"),
    )

    # Information about the degree
    alumnus          = models.ForeignKey(Alumnus, related_name="degrees")
    type             = models.CharField(max_length=3, choices=DEGREE_TYPE, default="PhD")
    date_start       = models.DateField(_("Starting date"), blank=True, null=True)
    date_stop        = models.DateField(_("Date finished"), blank=True, null=True)

    # Information about the thesis
    thesis_title = models.CharField(_("Thesis Title"), blank=True, max_length=180)
    date_of_defence  = models.DateField(_("Defence date"), blank=True, null=True, help_text=_("Date of the thesis or defense"))
    thesis_url       = models.URLField(blank=True, null=True, help_text=_("UvA DARE or other URL to thesis"))
    thesis_slug      = models.SlugField(blank=True, null=True, max_length=100, unique=True)
    # thesis_advisor   = models.ManyToManyField("self", symmetrical=False, through=StudentSupervisorRelationship)
    thesis_advisor   = models.ManyToManyField(Alumnus, blank=True, related_name="students")
    thesis_in_library= models.BooleanField(blank=True, default=False)
    comments         = models.TextField(_("comments"), blank=True)

    # students supervised --> class? anders kan je er maar een paar invullen
    # privacy levels

    class Meta:
        verbose_name = _("Degree")
        verbose_name_plural = _("Degrees")

    def __str__(self):
        return self.thesis_title

    def save(self, *args, **kwargs):
        MAXCOUNT = 100
        count = 0
        base_slug = slugify(self.thesis_title)
        self.thesis_slug = base_slug
        # The following loop should prevent a DB exception when
        # two people enter the same title at the same time
        while count < MAXCOUNT:
            try:
                super(Degree, self).save(*args, **kwargs)
            except IntegrityError:
                count += 1
                self.thesis_slug = base_slug + "_{0}".format(count)
            else:
                break

    @models.permalink
    def get_absolute_url(self):
        return ("alumnus:thesis-detail", [self.thesis_slug], {})

    @property
    def author(self):
        return self.alumnus.full_name

    @property
    def thesis_type(self):
        return self.type


@python_2_unicode_compatible
class PostdocPosition(models.Model):
    #postdoc information @api
    alumnus             = models.ForeignKey(Alumnus, related_name="postdoc")
    date_start_postdoc  = models.DateField(_("date start postdoc"), blank=True, null=True)
    date_stop_postdoc   = models.DateField(_("date stop postdoc"), blank=True, null=True)
    #supervisors,
    #field,

    #privacy levels

    class Meta:
        verbose_name = _("PostDoc Position")
        verbose_name_plural = _("PostDoc Positions")

    def __str__(self):
        return self.alumnus.last_name


@python_2_unicode_compatible
class Job(models.Model):
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
    stop_date           = models.DateField(_("date start job"), blank=True, null=True)
    inside_academia     = models.PositiveSmallIntegerField(_("inside academia"), choices=outside_inside_choices, default=1)
    location_job        = models.PositiveSmallIntegerField(_("location job"), choices=location_job_choices, default=1)

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")

    def __str__(self):
        return self.alumnus.last_name

