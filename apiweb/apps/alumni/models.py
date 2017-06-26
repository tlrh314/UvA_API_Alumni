from __future__ import unicode_literals, absolute_import, division

import os
import os.path
from datetime import date

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible

from jsonfield import JSONField
from tinymce.models import HTMLField
from django_countries.fields import CountryField

from .storage import OverwriteStorage
from .managers import AlumniManager

def get_mugshot_location(instance, filename):
    """ the media directory is already included """
    return os.path.join("uploads", "alumni", "mugshots",
                        instance.username, filename)

def get_photo_location(instance, filename):
    """ the media directory is already included """
    return os.path.join("uploads", "alumni", "photos",
                        instance.username, filename)

def get_thesis_pdf_location(instance, filename):
    """ the media directory is already included """
    return os.path.join("uploads", "theses", instance.type, filename)

def get_thesis_photo_location(instance, filename):
    """ the media directory is already included """
    return os.path.join("uploads", "theses", instance.type, filename)



@python_2_unicode_compatible
class PositionType(models.Model):
    name = models.CharField(max_length=80, help_text=_(
        "Name of position (e.g., director, faculty staff, postdoc, "
        "PhD student, ...)"))
    plural = models.CharField(max_length=80, blank=True, help_text=_(
        "Full plural name, if this is not a simple appended 's'"))

    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Possible Type of Position at API")
        verbose_name_plural = _("Possible Types of Position at API")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PreviousPosition(models.Model):
    NOVA_NETWORK = (
        ("NW1", "Nova Network 1"),
        ("NW2", "Nova Network 2"),
        ("NW3", "Nova Network 3"),
        ("INS", "Instrumentation"),
    )

    FUNDING = (
        (0, "Unknown"), (1, "ASTRON"), (2, "UvA"), (3, "SRON"), (4, "EC"),
        (5, "NOVA"), (6, "NWO"), (7, "VU"),  (8, "KNAW"),
        (9, "Other"), (10, "UvA API"), (11, "UvA GRAPPA"),
    )

    alumnus          = models.ForeignKey("Alumnus", related_name="positions")
    date_start       = models.DateField(_("Starting date"), blank=True, null=True)
    date_stop        = models.DateField(_("Date finished"), blank=True, null=True)
    type             = models.ForeignKey(PositionType, related_name="alumnus_set",
        blank=True, null=True, on_delete=models.SET_NULL)
    nova             = models.CharField(max_length=3, choices=NOVA_NETWORK, blank=True)
    funding          = models.PositiveSmallIntegerField(_("Funding"), choices=FUNDING, default=0)
    funding_note     = models.CharField(_("Funding Note"), blank=True, max_length=40)
    funding_remark   = models.CharField(_("Funding Remark"), blank=True, max_length=40)
    fte_per_year     = JSONField(blank=True, default=[], help_text="Enter mapping from year to fte in valid JSON syntax")
    is_last          = models.BooleanField(_("Last Position at API"), default=False)

    comments         = models.TextField(_("comments"), blank=True)
    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True)
    last_updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
        on_delete=models.SET_NULL, related_name="prevpos_updated")

    class Meta:
        verbose_name = _("Previous Position at API")
        verbose_name_plural = _("Previous Position at API")

    def __str__(self):
        return self.type.name


@python_2_unicode_compatible
class AcademicTitle(models.Model):
    title           = models.CharField(_("title"), max_length=20)

    class Meta:
        verbose_name = _("Academic Title")
        verbose_name_plural = _("Academic Titles")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Alumnus(AbstractBaseUser, PermissionsMixin):
    """ Represents an alumnus of API. Since we extend the AbstractBaseUser
        we inherit the password, last_login, is_active fields. """

    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
        (4, "Prefer not to say"),
    )

    # Account information
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    show_person     = models.BooleanField(_("alumnus visible on website"), default=True)
    passed_away     = models.BooleanField(_("Deceased"), blank=True, default=False,
        help_text=_("If selected a cross will appear by the name of this alumnus on the website."))

    # Personal information
    academic_title  = models.ForeignKey(AcademicTitle, on_delete=models.SET_NULL, blank=True, null=True)
    initials        = models.CharField(_("initials"), blank=True, max_length=40)
    first_name      = models.CharField(_("first name"), blank=True, max_length=40)
    nickname        = models.CharField(_("nickname"), blank=True, max_length=40)
    middle_names    = models.CharField(_("middle names"), blank=True, max_length=120)
    prefix          = models.CharField(_("prefix"), blank=True, max_length=40)
    last_name       = models.CharField(_("last name"), max_length=40)
    gender          = models.PositiveSmallIntegerField(_("gender"), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date      = models.DateField(_("birth date"), blank=True, null=True)
    nationality     = CountryField(_("nationality"), blank=True)
    place_of_birth  = models.CharField(_("place of birth"), blank=True, max_length=40)
    student_id      = models.CharField(_("student_id"), blank=True, max_length=10)
    mugshot         = models.ImageField(_("mugshot"), upload_to=get_mugshot_location, blank=True, null=True)
    photo           = models.ImageField(_("photo"), upload_to=get_photo_location,storage=OverwriteStorage(), blank=True, null=True)
    biography       = HTMLField(_("biography"), blank=True, default="")
    slug            = models.SlugField(_("slug"), unique=True)

    # Contact information
    # TODO: at a later point in time remove blank=True, null=True and add unique=True for email addresses
    email           = models.EmailField(_("email"), blank=True, null=True)
    home_phone      = models.CharField(_("home telephone"), blank=True, max_length=40)
    mobile          = models.CharField(_("mobile"), blank=True, max_length=40)
    homepage        = models.URLField(_("homepage"), blank=True, null=True)
    facebook        = models.URLField(_("facebook"), blank=True, null=True)
    twitter         = models.URLField(_("twitter"), blank=True, null=True)
    linkedin        = models.URLField(_("linkedin"), blank=True, null=True)
    last_checked    = models.DateTimeField(_("Date Last Checked"), blank=True, null=True,
        help_text=_("Update this field if you know that the contact information is up-to-date."))

    # Address information
    address         = models.CharField(_("address"), blank=True, max_length=40)
    streetname      = models.CharField(_("streetname"),blank=True, max_length=40)
    streetnumber    = models.CharField(_("streetnumber"),blank=True, max_length=40)
    zipcode         = models.CharField(_("zipcode"), blank=True, max_length=40)
    city            = models.CharField(_("city"), blank=True, max_length=40)
    country         = CountryField(_("country"), blank=True)

    # Current position at API
    position        = models.ForeignKey(PositionType, blank=True, null=True,
        related_name="current_position", on_delete=models.SET_NULL)
    specification   = models.CharField(max_length=255, blank=True,
        help_text=_("Type of grant, or other indicator of funding"))
    office          = models.CharField(_("office"), blank=True, max_length=40)
    work_phone      = models.CharField(_("work telephone"), blank=True, max_length=40)
    ads_name        = models.CharField(_("ads name"), blank=True, max_length=40)

    # Extra information
    comments        = models.TextField(_("comments"), blank=True)
    date_created    = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated    = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    #Privacy options
    show_biography  = models.BooleanField(_("Show biography on personal page"), blank=True, default=False)
    show_facebook   = models.BooleanField(_("Show facebook on personal page"), blank=True, default=False)
    show_linkedin   = models.BooleanField(_("Show linkedin on personal page"), blank=True, default=False)
    show_twitter    = models.BooleanField(_("Show twitter on personal page"), blank=True, default=False)
    show_email      = models.BooleanField(_("Show email on personal page"), blank=True, default=False)
    show_homepage   = models.BooleanField(_("Show homepage on personal page"), blank=True, default=False)

    objects = AlumniManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("Alumnus")
        verbose_name_plural = _("Alumni")
        ordering = ("last_name", "first_name")

    def get_full_name(self):
        """ Required when extending AbstractBaseUser """
        full_name = "{0} {1}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Required when extending AbstractBaseUser """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Required when extending AbstractBaseUser (?) """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        count = Alumnus.objects.filter(slug__contains = self.slug).count()
        self.slug = "{0}_{1}".format(self.slug, str(count + 1))
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(Alumnus, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("alumni:alumnus-detail", args=[self.slug])

    @property
    def full_name(self):
        title_last = self.academic_title in AcademicTitle.objects.filter(title__in=["MA", "MSc", "BSc"])
        if self.academic_title:
            title = " "+str(self.academic_title) if title_last else str(self.academic_title)+" "
        else:
            title = ""

        return ("{}{}{}{}{}{}".format(title if not title_last else "",
            self.first_name+" " if self.first_name else "",
            self.initials+" " if not self.first_name else "",
            self.prefix+" " if self.prefix else "",
            self.last_name, title if title_last else ""))

    @property
    def full_name_no_title(self):
        return ("{}{}{}{}".format(
            self.first_name+" " if self.first_name else "",
            self.initials+" " if not self.first_name else "",
            self.prefix+" " if self.prefix else "",
            self.last_name))

    @property
    def age(self):
        TODAY = date.today()
        return "{}".format(int((TODAY-self.birth_date).days/365.0))


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
    thesis_title     = models.CharField(_("Thesis Title"), blank=True, max_length=180)
    date_of_defence  = models.DateField(_("Defence date"), blank=True, null=True, help_text=_("Date of the thesis or defense"))
    thesis_url       = models.URLField(blank=True, null=True, help_text=_("UvA DARE or other URL to thesis"))
    thesis_slug      = models.SlugField(blank=True, null=True, max_length=100, unique=True)
    thesis_advisor   = models.ManyToManyField(Alumnus, blank=True, related_name="students")
    dissertation_nr  = models.PositiveSmallIntegerField(_("PhD Dissertation Counter"), blank=True, null=True)
    # Slug is for url

    # TODO: set the maxlim for uploads to 30MB ?
    thesis_pdf       = models.FileField(_("Full Text (pdf)"),
        upload_to=get_thesis_pdf_location, blank=True, null=True)
    # thesis_abstract  = models.HTMLField(_("Abstract"), blank=True, null=True)
    thesis_photo     = models.ImageField(_("Thesis Photo"),
        upload_to=get_thesis_photo_location, blank=True, null=True)
    thesis_in_library= models.BooleanField(blank=True, default=False)

    comments         = models.TextField(_("comments"), blank=True)
    last_updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
        on_delete=models.SET_NULL, related_name="theses_updated")
    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    # students supervised --> class? anders kan je er maar een paar invullen
    # privacy levels

    class Meta:
        verbose_name = _("MSc and/or PhD Thesis at API")
        verbose_name_plural = _("MSc and/or PhD Theses at API")

    def __str__(self):
        return self.thesis_title

    def save(self, *args, **kwargs):
        # Get dissertation_nr and increment
        if self.type == "phd" and not self.dissertation_nr:
            dissertation_nr = 0
            for d in Degree.objects.all():  # ugly bruteforce
                if d.dissertation_nr and d.dissertation_nr > dissertation_nr:
                    dissertation_nr = d.dissertation_nr
            self.dissertation_nr = dissertation_nr + 1

        # Set slug as firstname-lastname-degreetype with clash-prevention
        MAXCOUNT = 100
        count = 0
        base_slug = slugify(self.alumnus.full_name_no_title + "-" + self.type)
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

    def get_absolute_url(self):
        return reverse("alumni:thesis-detail", args=[self.thesis_slug])

    @property
    def author(self):
        return self.alumnus.full_name

    @property
    def thesis_type(self):
        return self.type
