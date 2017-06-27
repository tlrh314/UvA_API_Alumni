from __future__ import unicode_literals, absolute_import, division

import filebrowser.sites

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from ajax_select import urls as ajax_select_urls

from apiweb.context_processors import contactinfo

from .survey.views import survey_success


admin.autodiscover()

handler404 = 'main.views.page_not_found'
handler500 = 'main.views.page_not_found'


urlpatterns = [
    url(r'^admin/filebrowser/', include(filebrowser.sites.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/password_reset/$', auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            extra_context = {
                "api_phonenumber_formatted": contactinfo(None)["api_phonenumber_formatted"],
                "secretary_email_address": contactinfo(None)["contactinfo"].secretary_email_address,
            },
            email_template_name='registration/password_reset_email.html',
            extra_email_context = {
                "api_phonenumber_formatted": contactinfo(None)["api_phonenumber_formatted"],
                "secretary_email_address": contactinfo(None)["contactinfo"].secretary_email_address,
            }
        ), name='password_reset'),
    url(r'^admin/', include('django.contrib.auth.urls')),
    url(r'^alumni/', include('apiweb.apps.alumni.urls', namespace='alumni')),
    url(r'^theses/', include('apiweb.apps.research.urls', namespace='research')),
    url(r'^interviews/', include('apiweb.apps.interviews.urls', namespace='interviews')),
    url(r'^search/', include('apiweb.apps.search.urls', namespace='search')),
    url(r'^survey/', include('apiweb.apps.survey.urls', namespace='survey')),
    url(r'^vis/', include('apiweb.apps.visualization.urls', namespace='vizualisation')),
    url(r'^', include('apiweb.apps.main.urls')),
]
