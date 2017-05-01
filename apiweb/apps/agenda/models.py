from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
import markdown


@python_2_unicode_compatible
class Entry(models.Model):
    """Represents a entry in the API Agenda."""

    title = models.CharField(_('title'), max_length=120, default="")
    is_public = models.BooleanField(
        _('show to others?'), default=True,
        help_text=_("Let other users see your entry"))
    body = models.TextField(_('text'), max_length=10000, blank=True, default="")
    body_html = models.TextField(_('actual html body'), max_length=16000,
                                 blank=True, editable=False, default="")
#   date = models.DateField(_('date of event'), default=datetime.date.today)
    date = models.DateField(_('date of event'))
    date_end = models.DateField(
        _('end date of event'), blank=True, null=True,
        help_text=_("End date of the event, if different from the start date"))
    creator = models.ForeignKey(User, related_name='creator')
    slug = models.SlugField(_('slug'), max_length=500, blank=False,
                            editable=False, unique=False)


    def save(self, *args, **kwargs):
        self.slug = '{}-{}-{}_{}'.format(self.date.year, self.date.month,
                                         self.date.day, slugify(self.title))
        self.body_html = markdown.markdown(
            self.body,
            ['footnotes', 'tables', 'def_list', 'headerid'],
            safe_mode="escape")
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"

    def __str__(self):
        if self.title:
            return str(self.creator) + " - " + self.title
        else:
            return str(self.creator)

    def get_absolute_url(self):
        return reverse('agenda:entry-detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})
