from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import Index2View, All2View, WikiPage2View

handler500 = 'apiweb.main.errorview.server_error'

urlpatterns = [
    url(r'^view/(?P<name>[-\w]+)/$',
        view=WikiPage2View.as_view(),
        name='view2'),
    url(r'^all/$',
        view=All2View.as_view(),
        name='all2'),
    url(r'^$',
        view=Index2View.as_view(),
        name='index2'),
]
