from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import IndexView, PizzaAboutView
from .views import PressView, PizzaView, EventsView, ColloquiumView
from .views import PressDetailView, PizzaDetailView, EventDetailView
from .views import ColloquiumDetailView, ColloquiumSummaryView
from ..main.views import DetailRedirectView
from .models import Colloquium, Press, Event, Pizza


handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^colloquium/detail/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=ColloquiumDetailView.as_view(),
        name='colloquium-detail'),
    url(r'^colloquium/detail/(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Colloquium),
        name='colloquium-redirect'),
    url(r'^colloquium/summary/$',
        view=ColloquiumSummaryView.as_view(),
        name='colloquium-summary'),
    url(r'^colloquium/$',
        view=ColloquiumView.as_view(),
        name='colloquium'),
    url(r'^events/detail/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=EventDetailView.as_view(),
        name='events-detail'),
    url(r'^events/detail/(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Event),
        name='events-redirect'),
    url(r'^events/$',
        view=EventsView.as_view(),
        name='events'),
    url(r'^press/detail/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=PressDetailView.as_view(),
        name='press-detail'),
    url(r'^press/detail/(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Press),
        name='press-redirect'),
    url(r'^press/$',
        view=PressView.as_view(),
        name='press'),
    url(r'^pizza/detail/(?P<pk>\d+)(?P<slug>[-\w]+)/$',
        view=PizzaDetailView.as_view(),
        name='pizza-detail'),
    url(r'^pizza/detail/(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Pizza),
        name='pizza-redirect'),
    url(r'^pizza/about$', PizzaAboutView.as_view(),
        name='pizza-about'),
    url(r'^pizza/$',
        view=PizzaView.as_view(),
        name='pizza'),
    url(r'^$',
        view=IndexView.as_view(),
        name='index'),
]
