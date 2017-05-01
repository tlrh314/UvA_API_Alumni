from __future__ import unicode_literals, absolute_import, division

from django.db import models


class WikiManager(models.Manager):
    """Add some event specific managers"""

    def get_queryset(self):
        return super(WikiManager, self).get_queryset().filter(is_visible=True)
