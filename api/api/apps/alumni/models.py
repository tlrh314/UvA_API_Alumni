from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class Person(models.Model):
    """ Represents an alumnus at API. """

    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Unknown'),
    )

    user = models.OneToOneField(User, unique=True, related_name='alumnus')
    show_person = models.BooleanField(_('person visible on website'), default=True)
    first_name = models.CharField(_('first name'), blank=True, max_length=40)
    prefix = models.CharField(_('prefix'), blank=True, max_length=40)
    last_name = models.CharField(_('last name'), max_length=40)
    slug = models.SlugField(_('slug'), unique=True)
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    title = models.CharField(_('title'), blank=True, max_length=40)
    initials = models.CharField(_('initials'), blank=True, max_length=40)

    comments = models.TextField(_('comments'), blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return u'{0}'.format(self.full_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)

class ContactDetails(models.Model):
    person = models.OneToOneField(Person, unique=True, related_name='address')
    address = models.CharField(_('address'), blank=True, max_length=40)
    zipcode = models.CharField(_('zipcode'), blank=True, max_length=40)
    city = models.CharField(_('city'), blank=True, max_length=40)
    country = models.CharField(_('country'), blank=True, max_length=40)
    home_phone = models.CharField(_('home telephone'), blank=True, max_length=40)
    work_phone = models.CharField(_('work telephone'), blank=True, max_length=40)
    mobile = models.CharField(_('mobile'), blank=True, max_length=40)
    office = models.CharField(_('office'), blank=True, max_length=40)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    homepage = models.URLField(_('homepage'), blank=True, null=True)
