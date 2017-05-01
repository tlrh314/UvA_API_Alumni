from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import JobsView, JobDetailView
from .models import Job
from ..main.views import DetailRedirectView

handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=JobDetailView.as_view(),
        name='detail'),
    url(r'^(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Job),
        name='redirect'),
    url(r'^$',
        view=JobsView.as_view(),
        name='index'),
]
