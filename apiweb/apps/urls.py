from ajax_select import urls as ajax_select_urls
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from filebrowser.sites import site

from apiweb.context_processors import contactinfo

admin.autodiscover()

handler404 = "apiweb.apps.main.views.page_not_found"
handler500 = "apiweb.apps.main.views.handler500"


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa F841


urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("admin/filebrowser/", site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("ajax_select/", include(ajax_select_urls)),
    path("admin/", admin.site.urls),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            extra_context={
                "api_phonenumber_formatted": contactinfo(None)[
                    "api_phonenumber_formatted"
                ],
                "secretary_email_address": contactinfo(None)[
                    "contactinfo"
                ].secretary_email_address,
            },
            email_template_name="registration/password_reset_email.html",
            extra_email_context={
                "api_phonenumber_formatted": contactinfo(None)[
                    "api_phonenumber_formatted"
                ],
                "secretary_email_address": contactinfo(None)[
                    "contactinfo"
                ].secretary_email_address,
            },
        ),
        name="password_reset",
    ),
    path("admin/", include("django.contrib.auth.urls")),
    path("alumni/", include("apiweb.apps.alumni.urls")),
    path("theses/", include("apiweb.apps.research.urls")),
    path("interviews/", include("apiweb.apps.interviews.urls")),
    path("search/", include("apiweb.apps.search.urls")),
    path("survey/", include("apiweb.apps.survey.urls")),
    path("visualization/", include("apiweb.apps.visualization.urls")),
    path("", include("apiweb.apps.main.urls")),
]
