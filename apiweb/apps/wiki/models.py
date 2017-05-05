from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
import markdown
from .managers import WikiManager


@python_2_unicode_compatible
class WikiPage(models.Model):
    # Note: since we're storing the wiki in a separate database,
    # we can't use foreign keys, and created_author and
    # modification_author have to be Charfields instead of ForeignKeys
    name = models.CharField(_('URL name'), max_length=256, blank=False)
    text = models.TextField(_('text'), blank=True)
    html = models.TextField(_('actual HTML'), blank=True, editable=False)
    creation_date = models.DateTimeField(_('date created'),
                                         auto_now_add=True, editable=False)
    creation_author = models.CharField(_('created by'), max_length=160,
                                       blank=True, editable=False)
    modification_date = models.DateTimeField(_('date last modified'),
                                             editable=False, blank=True,
                                             null=True)
    modification_author = models.CharField(_('last modified by'),
                                           max_length=160, blank=True,
                                           editable=False)
    visits = models.IntegerField(_('number of visits'), default=0,
                                 editable=False)
    is_category_page = models.BooleanField(_('page is a category page'),
                                           default=False)
    is_visible = models.BooleanField(_('page is visible'), default=True)

    objects = models.Manager()
    visible = WikiManager()

    class Meta:
        verbose_name = _('wiki page')
        verbose_name_plural = _('wiki pages')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        self.html = markdown.markdown(
            self.text, ['footnotes', 'tables', 'def_list', 'headerid'],
            safe_mode="escape")
        super(WikiPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('wiki:view', kwargs={'name': self.name})

    def get_absolute_url2(self):
        return reverse('wiki2:view2', kwargs={'name': self.name})
