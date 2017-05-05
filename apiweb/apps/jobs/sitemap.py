from __future__ import unicode_literals, absolute_import, division

from django.contrib.sitemaps import Sitemap
from .models import Job


class JobSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Job.objects.current()
