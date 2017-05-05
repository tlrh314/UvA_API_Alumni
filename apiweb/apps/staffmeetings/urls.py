from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import IndexView

handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^(?P<year>\d+)/$', view=IndexView.as_view(), name='index'),
    url(r'^$', view=IndexView.as_view(), name='index'),
]
