from ..jobs.sitemap import JobSitemap
from ..news.sitemap import ColloquiumSitemap, EventSitemap, PizzaSitemap, PressSitemap
from ..people.sitemap import PersonSitemap
from ..research.sitemap import ResearchSitemap

sitemaps = dict(
    colloquia=ColloquiumSitemap,
    lunchtalks=PizzaSitemap,
    events=EventSitemap,
    press=PressSitemap,
    jobs=JobSitemap,
    people=PersonSitemap,
    research=ResearchSitemap,
)
