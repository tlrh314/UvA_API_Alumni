from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import alumnus_list, alumnus_detail, thesis_list, thesis_detail, thesis_has_no_pdf
from ..main.views import DetailRedirectView


# handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^theses/$', view=thesis_list, name='thesis-list'),
    url(r'^theses/(?P<thesis_slug>.*)/$', thesis_detail, name='thesis-detail'),
    url(r'^theses/thesis_not_found$', thesis_has_no_pdf, name='thesis-has-no-pdf'),
    url(r'^$', view=alumnus_list, name='alumnus-list'),
    url(r'alumnus/(?P<slug>.*)/$', alumnus_detail, name='alumnus-detail'),
]
