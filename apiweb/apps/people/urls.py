from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import PersonListView, StaffListView, StudentListView
from .views import PositionListView, PersonDetailView, PositionRedirectView
from .models import Person
from ..main.views import DetailRedirectView
from .views import PositionRedirectView


handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^position/staff/$', view=StaffListView.as_view(), name='staff-list'),
    url(r'^position/students/$', view=StudentListView.as_view(), name='student-list'),
    url(r'^position/(?P<position>([^/]+))/$',
        view=PositionListView.as_view(), name='position-list'),
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        view=PersonDetailView.as_view(),
        name='person-detail'),
    # Redirect old links
    url(r'^(?P<position>(adjunct|postdoc|phd|emeritus|guest|developer))/$',
        view=PositionRedirectView.as_view()),
    url(r'^(?P<slug>[-\w]+)/$',
        view=DetailRedirectView.as_view(model=Person)),

    url(r'^$', view=PersonListView.as_view(), name='person-list'),
]
