from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import SearchView

handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^$', view=SearchView.as_view(), name='index'),
]
