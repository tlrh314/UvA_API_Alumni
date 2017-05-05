from __future__ import unicode_literals, absolute_import, division

from django.contrib.sitemaps import Sitemap
from .models import Person


class PersonSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Person.objects.filter(show_person=True)
