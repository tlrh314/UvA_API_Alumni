from __future__ import unicode_literals, absolute_import, division

from django.contrib.sitemaps import Sitemap
from .models import Press, Event, Colloquium, Pizza


class PressSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Press.objects.current(-180)


class EventSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Event.objects.current(180)


class ColloquiumSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Colloquium.objects.current(180)


class PizzaSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Pizza.objects.current(180)
