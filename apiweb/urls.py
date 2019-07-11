from __future__ import unicode_literals, absolute_import, division

import sys

from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import include, path, re_path


handler404 = "apiweb.apps.main.views.page_not_found"
handler500 = "apiweb.apps.main.views.handler500"

urlpatterns = [
    path("", include("apiweb.apps.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
