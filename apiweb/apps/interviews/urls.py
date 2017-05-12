from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'interviews/(?P<slug>.*)/$', views.detail, name='detail')
]
