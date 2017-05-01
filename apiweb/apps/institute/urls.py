from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import MapView, ContactView, InstituteView, NinetyYearsView

handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^90years/$', view=NinetyYearsView.as_view(), name='90years'),
    url(r'^contact/$', view=ContactView.as_view(), name='contact'),
    url(r'^map/$', view=MapView.as_view(), name='map'),
    url(r'^$', view=InstituteView.as_view(), name='index'),
]
