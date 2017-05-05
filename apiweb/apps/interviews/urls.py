from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^interview/$', views.interview, name='interview'),
    # url(r'^blog/group(?P<interview_category>.*)/$', views.interview, name='interview'),
    url(r'^inverview/(?P<slug>.*)/$', views.interview_post, name='interview_post')
]
