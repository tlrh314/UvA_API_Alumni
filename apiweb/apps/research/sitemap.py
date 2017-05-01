from __future__ import unicode_literals, absolute_import, division

from django.contrib.sitemaps import Sitemap
from .models import ResearchTopic


class ResearchSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return ResearchTopic.objects.all()
