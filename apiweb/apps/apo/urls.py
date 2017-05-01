from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from django.views.generic import RedirectView
from .views import FiftyOneView, SolarView, GalleryView, PracticumView
from .views import IndexView, ImageView


handler500 = 'apiweb.apps.main.errorview.server_error'


urlpatterns = [
    url(r'^51cm/$', view=FiftyOneView.as_view(), name='51cm'),
    url(r'^solar/$', view=SolarView.as_view(), name='solar'),
    url(r'^gallery/$', view=GalleryView.as_view(), name='gallery'),
    url(r'^gallery/image/$', view=RedirectView.as_view(url='/apo/gallery/')),
    url(r'^gallery/image/(?P<id>\d+)/$', view=ImageView.as_view(),
        name='gallery-image'),
    url(r'^practicum/$', view=PracticumView.as_view(), name='practicum'),
    url(r'^$', view=IndexView.as_view(), name='index'),
]
