from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import IndexView, AllView, WikiPageView
from .views import WikiCreateView, WikiEditView, WikiDeleteView

handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^view/(?P<name>[-\w]+)/$',
        view=WikiPageView.as_view(),
        name='view'),
    url(r'^edit/(?P<name>[-\w]+)/$',
        view=WikiEditView.as_view(),
        name='edit'),
    url(r'^delete/(?P<name>[-\w]+)/$',
        view=WikiDeleteView.as_view(),
        name='delete'),
    url(r'^create/$',
        view=WikiCreateView.as_view(),
        name='create'),
    url(r'^all/$',
        view=AllView.as_view(),
        name='all'),
    url(r'^$',
        view=IndexView.as_view(),
        name='index'),
]
