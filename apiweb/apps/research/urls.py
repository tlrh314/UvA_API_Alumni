from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import LinksView, IndexView, CategoryView
from .views import TopicView, GrbSoftwareView, ThesisView
from ..main.views import DetailRedirectView
from .models import ResearchTopic


handler500 = 'apiweb.apps.main.errorview.server_error'

categories = "|".join(["compacts", "cosmics", "astroparticles",
                       "planets", "stars"])
urlpatterns = [
    url(r'^cosmics/gamma-ray-bursts/software/$',
        view=GrbSoftwareView.as_view(),
        name='grbsoftware'),
    url(r'^(?P<category_type>(' + categories +
        r'))/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=TopicView.as_view(),
        name='topic'),
    url(r'^(?P<category_type>(' + categories + '))/(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=ResearchTopic),
        name='redirect'),
    url(r'^(?P<category_type>(' + categories + '))/$',
        view=CategoryView.as_view(),
        name='category'),
    url(r'^theses_(?P<thesis_type>(phd|msc|bsc))/$',
        view=ThesisView.as_view(),
        name='thesis'),
    url(r'^links/$',
        view=LinksView.as_view(),
        name='links'),
    url(r'^$',
        view=IndexView.as_view(),
        name='index'),
]
