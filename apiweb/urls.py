from __future__ import unicode_literals, absolute_import, division

import sys

from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views import defaults as default_views


handler404 = "apiweb.apps.main.views.page_not_found"
handler500 = "apiweb.apps.main.views.handler500"

urlpatterns = [
    path("", include("apiweb.apps.urls"))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
