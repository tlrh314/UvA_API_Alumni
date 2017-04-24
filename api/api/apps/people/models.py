from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models import permalink
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from ..research.models import ResearchTopic
import os
import os.path



def get_mugshot_location(instance, filename):
    return os.path.join("uploads", "images", "people", "mugshots",
                        instance.user.username, filename)


def get_photo_location(instance, filename):
    return os.path.join("uploads", "images", "people", "photos",
                        instance.user.username, filename)


class Person(models.Model):
    """ Represents a person at API. """

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

    user = models.OneToOneField(User, unique=True, related_name='person')
    show_person = models.BooleanField(_('person visible on website'), default=True)
    first_name = models.CharField(_('first name'), blank=True, max_length=40)
    prefix = models.CharField(_('prefix'), blank=True, max_length=40)
    last_name = models.CharField(_('last name'), max_length=40)
    slug = models.SlugField(_('slug'), unique=True)
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    title = models.CharField(_('title'), blank=True, max_length=40)
    initials = models.CharField(_('initials'), blank=True, max_length=40)
    ads_name = models.CharField(_('ads name'), blank=True, max_length=40)
    address = models.CharField(_('address'), blank=True, max_length=40)
    zipcode = models.CharField(_('zipcode'), blank=True, max_length=40)
    city = models.CharField(_('city'), blank=True, max_length=40)
    country = models.CharField(_('country'), blank=True, max_length=40)
    home_phone = models.CharField(_('home telephone'), blank=True, max_length=40)
    work_phone = models.CharField(_('work telephone'), blank=True, max_length=40)
    mobile = models.CharField(_('mobile'), blank=True, max_length=40)
    office = models.CharField(_('office'), blank=True, max_length=40)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    position = models.PositiveSmallIntegerField(_('position'), choices=POSITION_OPTIONS, default=5)
    mugshot = models.ImageField(_('mugshot'), upload_to=get_mugshot_location, blank=True, null=True)
    photo = models.ImageField(_('photo'), upload_to=get_photo_location, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    homepage = models.URLField(_('homepage'), blank=True, null=True)
    research = models.ManyToManyField(
        ResearchTopic, verbose_name=_("research"), blank=True, related_name='interest')
    contact = models.ManyToManyField(
        ResearchTopic, verbose_name=_("contact"), blank=True, related_name='contact')
    comments = models.TextField(_('comments'), blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return u'%s' % self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        try:
            # Work around a nasty bug in Django: don't use user=self.user
            # Also: is user__username better than user__pk?
            Person.objects.exclude(
                user__username=self.user.username).get(slug=self.slug)
        except ObjectDoesNotExist:
            pass
        else:
            count = Person.objects.filter(slug__contains = self.slug).count()
            self.slug = '%s_%s' % (self.slug, str(count + 1))
        os.umask(0o002)  # change umask so created (sub)directories
                         # have correct permissions
        super(Person, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('people:person-detail', None, {'slug': self.slug})

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return (u'%s %s %s' % (
            self.first_name, self.prefix, self.last_name)).replace("  ", " ")

    @property
    def age(self):
        TODAY = date.today()
        return u'%d' % int((TODAY-self.birth_date).days/365.0)

