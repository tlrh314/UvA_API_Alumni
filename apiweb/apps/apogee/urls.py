from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import IndexView, MonthView, WeekView, EntryDetailView
from .views import EntryCreateView, EntryUpdateView, EntryDeleteView
from ..main.views import DetailRedirectView
from .models import Entry


handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^detail/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=EntryDetailView.as_view(),
        name='entry-detail'),
    url(r'^detail/(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Entry),
        name='entry-redirect'),
    url(r'^update/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=EntryUpdateView.as_view(),
        name='entry-update'),
    url(r'^delete/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=EntryDeleteView.as_view(),
        name='entry-delete'),
    url(r'^create/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        view=EntryCreateView.as_view(),
        name='entry-create'),
    url(r'^month/(?P<year>\d+)/(?P<month>\d+)/(?P<change>(prev|next))/$',
        view=MonthView.as_view(),
        name='month'),
    url(r'^month/(?P<year>\d+)/(?P<month>\d+)/$',
        view=MonthView.as_view(),
        name='month'),
    url(r'^month/$',
        view=MonthView.as_view(),
        name='month'),
    url(r'^week/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/'
        '(?P<change>(prev|next))/$',
        view=WeekView.as_view(),
        name='week'),
    url(r'^week/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        view=WeekView.as_view(),
        name='week'),
    url(r'^week/$',
        view=WeekView.as_view(),
        name='week'),
    url(r'^(?P<year>\d+)/$',
        view=IndexView.as_view(),
        name='index'),
    url(r'^$',
        view=IndexView.as_view(),
        name='index'),
]
