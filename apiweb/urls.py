from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import include, url
from django.conf import settings
import django.views.static
import sys


handler500 = 'apiweb.apps.main.errorview.server_error'


# Hack to enable the development server to find the media files,
# while keeping those files in the same place as the rest of the
# development
if 'runserver' in sys.argv:
    urlpatterns = [
        # special URLs
        # url(r'^media/uploads/staff_meetings/',
        #     include('apiweb.apps.staffmeetings.media_urls')),
        url(r'^media/(?P<path>.*)$',
            django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^(?P<path>robots.txt)$',
            django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),

        # normal URLs
        url(r'^', include('apiweb.apps.urls')),
    ]
else:
    urlpatterns = [url(r'^', include('apiweb.apps.urls'))]
