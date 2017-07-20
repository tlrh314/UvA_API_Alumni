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
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
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
        help_text=_("If selected an asterisk will appear by the name of this alumnus on the website."))

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
    mugshot         = models.ImageField(_("mugshot"), upload_to=get_mugshot_location, storage=OverwriteStorage(), blank=True, null=True)
    biography       = HTMLField(_("biography"), blank=True, default="")
    slug            = models.SlugField(_("slug"), unique=True)

    # Contact information
    # TODO: at a later point in time remove null=True and add unique=True for email addresses
    email           = models.EmailField(_("email"),blank=True, null=True)
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
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = _("Alumnus")
        verbose_name_plural = _("Alumni")
        ordering = ("last_name", "first_name")

    def get_full_name(self):
        """ Required when extending AbstractBaseUser """
        title_last = self.academic_title in AcademicTitle.objects.filter(title__in=["MA", "MSc", "BSc", "PhD"])
        if self.academic_title:
            title = " "+str(self.academic_title) if title_last else str(self.academic_title)+" "
        else:
            title = ""

        return ("{}{}{}{}{}{}".format(title if not title_last else "",
            self.first_name+" " if self.first_name else "",
            self.initials+" " if not self.first_name else "",
            self.prefix+" " if self.prefix else "",
            self.last_name, title if title_last else ""))

    def get_short_name(self):
        """ Required when extending AbstractBaseUser """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Required when extending AbstractBaseUser (?) """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        MAXCOUNT = 100
        count_s, count_u, count = 0, 0, 0
        base_slug = slugify(self.full_name_no_title)
        self.slug = base_slug
        while count_s < MAXCOUNT and count_u < MAXCOUNT and count < MAXCOUNT:
            try:
                super(Alumnus, self).save(*args, **kwargs)
            except IntegrityError as e:
                count += 1
                # Fix for both sqlite3 and MySQL
                if "UNIQUE constraint failed: alumni_alumnus.username" in str(e) \
                    or ( "Duplicate entry" in str(e) and "for key 'username'" in str(e)):
                    count_u += 1
                    self.username += "_{0}".format(count_u)
                if "UNIQUE constraint failed: alumni_alumnus.slug" in str(e) \
                    or ( "Duplicate entry" in str(e) and "for key 'username'" in str(e)):
                    count_s += 1
                    self.slug = base_slug + "_{0}".format(count_s)

            else:
                break

    def get_absolute_url(self):
        return reverse("alumni:alumnus-detail", args=[self.slug])

    @property
    def full_name(self):
        return self.get_full_name()

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
