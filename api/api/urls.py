from __future__ import unicode_literals, absolute_import, division
import sys

from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
#from django.conf.urls.static import static
import django.views.static

handler500 = 'api.apps.main.errorview.server_error'

# Hack to enable the development server to find the media files,
# while keeping those files in the same place as the rest of the
# development
urlpatterns = []
if 'runserver' in sys.argv:
    urlpatterns += [
        # special URLs
        url(r'^media/(?P<path>.*)$',
            django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^(?P<path>robots.txt)$',
            django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),
        ]

# Normal URLs
urlpatterns += [
    url(r'^', include('api.apps.alumni.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('api.apps.blog.urls')),
    url(r'^institute/', include('api.apps.institute.urls', namespace='institute')),
    url(r'^people/', include('api.apps.people.urls', namespace='people')),
    url(r'^tinymce/', include('tinymce.urls')),
]
