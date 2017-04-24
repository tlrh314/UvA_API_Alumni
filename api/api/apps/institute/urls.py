from django.conf.urls import url, handler404
from . import views
from .views import MapView, ContactView, InstituteView

handler500 = 'api.apps.main.errorview.server_error'

app_name = 'institute'
urlpatterns = [
    url(r'^contact/$', view=ContactView.as_view(),     name='contact'),
    url(r'^map/$',     view=MapView.as_view(),         name='map'),
    url(r'^$',         view=InstituteView.as_view(),   name='index'),
]

