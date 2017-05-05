from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class BookCategory(models.Model):
    """Represents a category for a book at API."""

    category = models.CharField(_('book category'), unique=True, max_length=100)

    class Meta:
        verbose_name = _('book category')
        verbose_name_plural = _('book categories')
        ordering = ('category',)

    def __str__(self):
        return str(self.category)


@python_2_unicode_compatible
class Book(models.Model):
    """Represents a book at API."""

    BOOK_STATUS = (
        ('present', 'Present'),
        ('missing', 'Missing'),
        ('on_loan', 'On Loan'),
    )

    authors = models.CharField(_('authors'), max_length=100)
    title = models.CharField(_('title'), max_length=160,
                             default=_("Title Unknown"))
    year = models.PositiveIntegerField(_('year'), blank=True, null=True)
    label = models.CharField(_('label'), unique=True, max_length=40)
    status = models.CharField(max_length=16, choices=BOOK_STATUS,
                              default='Present')
    category = models.ManyToManyField(BookCategory,
                                      verbose_name=_("book category"),
                                      blank=True)

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
        ordering = ('authors', 'title')

    def __str__(self):
        return str(self.label)


@python_2_unicode_compatible
class Proceeding(models.Model):
    """Represents a proceeding at API."""

    PROCEEDING_STATUS = (
        ('present', 'Present'),
        ('missing', 'Missing'),
        ('on_loan', 'On Loan'),
    )

    authors = models.CharField(_('authors'), max_length=100)
    title = models.CharField(_('title'), unique=True, max_length=160,
                             default=_("Title Unknown"))
    year = models.PositiveIntegerField(_('year'), blank=True, null=True)
    label = models.CharField(_('label'), max_length=40)
    status = models.CharField(max_length=16, choices=PROCEEDING_STATUS,
                              default='Present')

    class Meta:
        verbose_name = _('proceeding')
        verbose_name_plural = _('proceedings')
        ordering = ('authors', 'title')

    def __str__(self):
        return str(self.title)


@python_2_unicode_compatible
class PhDThesis(models.Model):
    """Represents a Phd thesis from another university at API."""

    PHD_STATUS = (
        ('present', 'Present'),
        ('missing', 'Missing'),
        ('on_loan', 'On Loan'),
    )

    author = models.CharField(_('author'), unique=True, max_length=100)
    title = models.CharField(_('title'), max_length=160,
                             default=_("Title Unknown"))
    year = models.PositiveIntegerField(_('year'), blank=True, null=True)
    university = models.CharField(_('university'), max_length=40)
    status = models.CharField(max_length=16, choices=PHD_STATUS,
                              default='Present')

    class Meta:
        verbose_name = _('phd thesis')
        verbose_name_plural = _('phd theses')
        ordering = ('author', 'title')

    def __str__(self):
        return str(self.title)
