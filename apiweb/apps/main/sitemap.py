from __future__ import unicode_literals, absolute_import, division

from ..news.sitemap import EventSitemap, PressSitemap
from ..news.sitemap import ColloquiumSitemap, PizzaSitemap
from ..research.sitemap import ResearchSitemap
from ..people.sitemap import PersonSitemap
from ..jobs.sitemap import JobSitemap


sitemaps = dict(
    colloquia=ColloquiumSitemap,
    lunchtalks=PizzaSitemap,
    events=EventSitemap,
    press=PressSitemap,
    jobs=JobSitemap,
    people=PersonSitemap,
    research=ResearchSitemap)
