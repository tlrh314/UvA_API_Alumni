from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import BachelorProjectView, MasterProjectView, CourseView
from .views import ProjectsBachelorView, ProjectsMasterView, ProjectsView
from .views import BachelorView, MasterView, IndexView
from ..main.views import DetailRedirectView
from .models import BachelorProject, MasterProject


handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^bachelor/projects/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        BachelorProjectView.as_view(),
        name='bachelor-projects-detail'),
    url(r'^bachelor/projects/(?P<slug>[-\w]+)/$',
        DetailRedirectView.as_view(model=BachelorProject),
        name='bachelor-projects-redirect'),
    url(r'^master/projects/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        MasterProjectView.as_view(),
        name='master-projects-detail'),
    url(r'^master/projects/(?P<slug>[-\w]+)/$',
        DetailRedirectView.as_view(model=MasterProject),
        name='master-projects-redirect'),
    url(r'^projects/bachelor/$',
        ProjectsBachelorView.as_view(),
        name='bachelor-projects'),
    url(r'^projects/master/$',
        ProjectsMasterView.as_view(),
        name='master-projects'),
    url(r'^course/(?P<slug>[-\w]+)/$',
        CourseView.as_view(),
        name='course-topic-detail'),
    url(r'^projects/$',
        ProjectsView.as_view(),
        name='projects-index'),
    url(r'^bachelor/$',
        BachelorView.as_view(),
        name='bachelor'),
    url(r'^master/$',
        MasterView.as_view(),
        name='master'),
    url(r'^$',
        IndexView.as_view(),
        name='index'),
]
