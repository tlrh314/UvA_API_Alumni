from __future__ import unicode_literals, absolute_import, division

import filebrowser.sites

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from ajax_select import urls as ajax_select_urls
import django.contrib.sitemaps.views

from .main.views import index, contact, contact_success


admin.autodiscover()

handler404 = 'main.views.page_not_found'
handler500 = 'main.views.page_not_found'

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html')),
    url(r'^admin/filebrowser/', include(filebrowser.sites.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('django.contrib.auth.urls')),

    url(r'^alumni/', include('apiweb.apps.alumni.urls', namespace='alumni')),
    url(r'^interviews/', include('apiweb.apps.interviews.urls', namespace='interviews')),
    url(r'^contact/$', contact, name='contact'),
    url(r'^thanks/$', contact_success, name='contact_success'),
    url(r'^search/', include('apiweb.apps.search.urls', namespace='search')),
    url(r'^vis/', include('apiweb.apps.visualization.urls', namespace='vizualisation')),
    url(r'^$', index, name='index'),

    # TODO: clean up code below

    # url(r'^.*[A-Z]+.*$',
    #     view=LowercaseView.as_view(),
    #     name='redirect-uppercase'),

    # url(r'^media/uploads/staff_meetings/',
    #     include('apiweb.apps.staffmeetings.media_urls')),

    # redirects
    # url(r'^scatter/(?P<arguments>.*)$',
    #     view=ScatterView.as_view(),
    #     name='scatter'),
    # url(r'^home2.html$',
    #     view=HomeView.as_view(),
    #     name='home2'),
    # url(r'^home.html$',
    #     view=HomeView.as_view(),
    #    name='home'),

    # url(r'^people/',
    #     include('apiweb.apps.people.urls', namespace='people')),
    # url(r'^news/',
    #     include('apiweb.apps.news.urls', namespace='news')),
    # url(r'^education/',
    #     include('apiweb.apps.education.urls', namespace='education')),
    # url(r'^institute/',
    #     include('apiweb.apps.institute.urls', namespace='institute')),
    # url(r'^library/',
    #     include('apiweb.apps.library.urls', namespace='library')),
    # url(r'^research/',
    #     include('apiweb.apps.research.urls', namespace='research')),
    # url(r'^publiek/',
    #     include('apiweb.apps.publiek.urls', namespace='publiek')),
    # url(r'^jobs/',
    #     include('apiweb.apps.jobs.urls', namespace='jobs')),
    # url(r'^apo/',
    #     include('apiweb.apps.apo.urls', namespace='apo')),
    # url(r'^internal/account/',
    #     include('apiweb.apps.internal.account_urls', namespace='account')),
    # url(r'^internal/staffmeetings/',
    #     include('apiweb.apps.staffmeetings.urls', namespace='staffmeetings')),
    # url(r'^internal/agenda/',
    #     include('apiweb.apps.agenda.urls', namespace='agenda')),
    # url(r'^internal/apogee/',
    #     include('apiweb.apps.apogee.urls', namespace='apogee')),
    # url(r'^internal/wiki/',
    #     include('apiweb.apps.wiki.urls', namespace='wiki')),
    # url(r'^internal/',
    #     include('apiweb.apps.internal.urls', namespace='internal')),
    # url(r'^wiki/',
    #     include('apiweb.apps.wiki.viewonly_urls', namespace='wiki2')),
    # url(r'^sitemap/', view=SitemapView.as_view(),
    #     name='sitemap'),
    # url(r'^sitemap\.xml$',
    #     django.contrib.sitemaps.views.sitemap,
    #     {'sitemaps': sitemaps}),
    # url(r'^about/$',
    #     view=AboutView.as_view(), name='about'),
    # url(r'^24/7/$',
    #     view=TwentyFourSevenView.as_view(), name='247'),
    # url(r'^old/',
    #     include('apiweb.apps.old.urls', namespace='old')),
]
