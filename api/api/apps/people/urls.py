from django.conf.urls import include, url, handler404
from .views import PersonListView, StaffListView, StudentListView
from .views import PositionListView, PersonDetailView

handler500 = 'api.apps.main.errorview.server_error'

urlpatterns = [
   url(r'^staff/$', view=StaffListView.as_view(), name='staff-list'),
   url(r'^students/$', view=StudentListView.as_view(), name='student-list'),
   url(r'^(?P<position_type>(adjunct|postdoc|phd|emeritus|guest|developer))/$',
                       view=PositionListView.as_view(), name='position-list'),
   url(r'^(?P<slug>[-\w]+)/$',
                       view=PersonDetailView.as_view(), name='person-detail'),
   url(r'^$', view=PersonListView.as_view(), name='person-list'),
]
