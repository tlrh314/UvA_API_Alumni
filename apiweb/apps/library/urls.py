from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import IndexView, ProceedingsView, PhDView

handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^phdtheses/$', view=PhDView.as_view(), name='phdtheses'),
    url(r'^proceedings/$', view=ProceedingsView.as_view(), name='proceedings'),
    url(r'^$', view=IndexView.as_view(), name='index'),
]
