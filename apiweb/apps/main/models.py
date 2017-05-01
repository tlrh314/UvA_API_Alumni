from django.db import models
from django.utils.translation import ugettext_lazy as _


class Sticky(models.Model):
    PRIORITIES = ((0, 'high'),
                  (1, 'normal'),
                  (2, 'low'))
    title = models.CharField(max_length=160)
    url = models.CharField(max_length=500)
    priority = models.IntegerField(choices=PRIORITIES, default=0,
                                   help_text="Higher priority items will be "
                                   "first in the list of stickies")
    visible = models.BooleanField(_("visible on site"), default=True)

    class Meta:
        verbose_name_plural = "stickies"
