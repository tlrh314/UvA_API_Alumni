from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import CheckFileView

handler500 = 'apiweb.main.errorview.server_error'

urlpatterns = [
    url(r'^(?P<path>.*)$', view=CheckFileView.as_view(), name='check-file'),
]
