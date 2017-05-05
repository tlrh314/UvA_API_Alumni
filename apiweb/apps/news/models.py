from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from .managers import EventManager
from ...settings import MEDIA_ROOT
import datetime
import os
import re


def clean_text(text):
    """

    Removes all <span.*> and </span> attributes.

    This should make life a bit easier when copy-pasting into a text
    field that is augmented by tiny_mce: the layout of the pasted text
    should conform much better to the overall layout after removal of
    the span tag.

    """

    # remove <span> tags
    text = re.sub(r'</?span[^>]*>', '', text)
    ## remove style attributes inside other tags
    #text = re.sub(r'(?P<tagstart><[^>]+?)style="[^"]*"', '\g<tagstart>', text)
    return text


def save_teaser_picture(instance, filename):
    """Determine upload path for teaser pictures

    The instance's _meta attribute carries the verbose name.
    Verbose names are therefore explicitly defined for the BaseEvent class
    and each derived class
    Path names are dependent on the class, and will have increasing
    numbering if files with similar names exist

    """

    MAXCOUNT = 100
    subdir = instance._meta.verbose_name_raw
    if instance._meta.verbose_name_raw == 'base event':
        subdir = "base"
    elif instance._meta.verbose_name_raw == 'pizza lunch talk':
        subdir = "pizza"
    fullpath = os.path.join("uploads/images/news", subdir, filename)
    basename, ext = os.path.splitext(fullpath)
    count = 0
    while count < MAXCOUNT:
        if os.path.exists(os.path.join(MEDIA_ROOT, fullpath)):
            count += 1
            fullpath = "{}_{}{}".format(basename, count, ext)
        else:
            break
    return fullpath


@python_2_unicode_compatible
class BaseEvent(models.Model):
    """Abstract base class that serves for various items, such as
    news items, events, talks etc

    """

    title = models.CharField(max_length=160, default=_("Title not yet known"))
    text = models.TextField(blank=True)
    date = models.DateField(help_text=_("date of the event, if any"))
    date_end = models.DateField(blank=True, null=True,
                                help_text=_("end date of the event, if "
                                            "different from the start date"))
    time = models.TimeField(blank=True, null=True,
                            help_text=_("time of the event, if any"))
    time_end = models.TimeField(blank=True, null=True,
                                help_text=_("end time of the event, when "
                                            "required"))
    location = models.CharField(max_length=80, default="",
                                blank=True)
    teaser_text = models.TextField(blank=True,
                                   help_text=_("one or two short sentences for "
                                               "on the front page"))
    teaser_picture = models.ImageField(
        upload_to=save_teaser_picture, blank=True, null=True,
        help_text=_("Small (100x100 pixels maximum) picture for on the "
                    "front page"))
    visible = models.BooleanField(_('visible on site'), default=True,
                                  help_text=_(
                                      "Explicitly turn visibility for an item "
                                      "on or off. When visibility is turned "
                                      "on, behaviour follows the on/off dates"))
    date_on = models.DateField(
        help_text=_("date from which the item is visible on the site "
                    "(inclusive)"))
    date_off = models.DateField(
        help_text=_(
            "date until which the item is visible on the site (inclusive)"))
    slug = models.SlugField(max_length=500, blank=False, unique=False)

    # We've added a method to EventManager, but not overridden any old method
    # So, we can safely assign EventManager to objects (the default manager)
    objects = EventManager()

    class Meta:
        abstract = True
        verbose_name = _("base event")
        verbose_name_plural = _("base events")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.text = clean_text(self.text)
        self.slug = slugify(self.title)
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(BaseEvent, self).save(*args, **kwargs)

    def upcoming(self):
        return self.date >= datetime.date.today()


    def past_due(self):
        if self.date < datetime.date.today():
            return True
        return False

    def date_time(self):
        """Combine date & time into one, even if time is not given.

        In such a case, we set the time to be 1 minute past midnight
        """

        time = datetime.time(0, 0, 1) if self.time is None else self.time
        return datetime.datetime.combine(self.date, time)


class NewsItem(BaseEvent):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('nl', 'Dutch'),
        )
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES,
                                default='en', help_text=_(
                                    "Language that is used in the item text"))

    class Meta:
        abstract = True
        verbose_name = _("news item")
        verbose_name_plural = _("news items")


class Talk(BaseEvent):
    speaker = models.CharField(max_length=80)
    affiliation = models.CharField(max_length=120, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("talk")
        verbose_name_plural = _("talks")


class Press(NewsItem):

    class Meta:
        verbose_name = _("press")
        verbose_name_plural = _("press")

    def get_absolute_url(self):
        return reverse('news:press-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})


@python_2_unicode_compatible
class Event(NewsItem):

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:events-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})


@python_2_unicode_compatible
class Colloquium(Talk):

    class Meta:
        verbose_name = _("colloquium")
        verbose_name_plural = _("colloquia")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:colloquium-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})


@python_2_unicode_compatible
class Pizza(Talk):
    shorttalk_speaker = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = _("pizza lunch talk")
        verbose_name_plural = _("pizza lunch talks")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:pizza-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})
