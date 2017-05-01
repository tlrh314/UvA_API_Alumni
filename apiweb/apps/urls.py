from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.sitemaps.views
from .main.sitemap import sitemaps
from .main.views import MainView, HomeView, ScatterView, LowercaseView
from .main.views import SitemapView, AboutView, TwentyFourSevenView
import filebrowser.sites


admin.autodiscover()

urlpatterns = [
    url(r'^.*[A-Z]+.*$',
        view=LowercaseView.as_view(),
        name='redirect-uppercase'),

    url(r'^media/uploads/staff_meetings/',
        include('apiweb.apps.staffmeetings.media_urls')),

    url(r'^admin/filebrowser/',
        include(filebrowser.sites.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),

    #url(r'^admin/filebrowser/',
    #    include('filebrowser.urls', namespace='filebrowser')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # deprecated url(r'^admin/(.*)', admin.site.root, name='admin-root'),
    # to use new setup in templates, use {% url admin:index %}
    url(r'^admin/',
        include(admin.site.urls)),

    url(r'^news/',
        include('apiweb.apps.news.urls', namespace='news')),
    url(r'^people/',
        include('apiweb.apps.people.urls', namespace='people')),
    url(r'^education/',
        include('apiweb.apps.education.urls', namespace='education')),
    url(r'^institute/',
        include('apiweb.apps.institute.urls', namespace='institute')),
    url(r'^library/',
        include('apiweb.apps.library.urls', namespace='library')),
    url(r'^research/',
        include('apiweb.apps.research.urls', namespace='research')),
    url(r'^publiek/',
        include('apiweb.apps.publiek.urls', namespace='publiek')),
    url(r'^jobs/',
        include('apiweb.apps.jobs.urls', namespace='jobs')),
    url(r'^apo/',
        include('apiweb.apps.apo.urls', namespace='apo')),
    url(r'^internal/account/',
        include('apiweb.apps.internal.account_urls', namespace='account')),
    url(r'^internal/staffmeetings/',
        include('apiweb.apps.staffmeetings.urls', namespace='staffmeetings')),
    url(r'^internal/agenda/',
        include('apiweb.apps.agenda.urls', namespace='agenda')),
    url(r'^internal/apogee/',
        include('apiweb.apps.apogee.urls', namespace='apogee')),
    url(r'^internal/wiki/',
        include('apiweb.apps.wiki.urls', namespace='wiki')),
    url(r'^internal/',
        include('apiweb.apps.internal.urls', namespace='internal')),
    url(r'^wiki/',
        include('apiweb.apps.wiki.viewonly_urls', namespace='wiki2')),
    url(r'^sitemap/', view=SitemapView.as_view(),
        name='sitemap'),
    url(r'^sitemap\.xml$',
        django.contrib.sitemaps.views.sitemap,
        {'sitemaps': sitemaps}),
    url(r'^search/',
        include('apiweb.apps.search.urls', namespace='search')),
    url(r'^about/$',
        view=AboutView.as_view(), name='about'),
    url(r'^24/7/$',
        view=TwentyFourSevenView.as_view(), name='247'),
    url(r'^old/',
        include('apiweb.apps.old.urls', namespace='old')),
    url(r'^alumni/',
        include('apiweb.apps.alumni.urls', namespace='alumni')),

    # redirects
    url(r'^scatter/(?P<arguments>.*)$',
        view=ScatterView.as_view(),
        name='scatter'),
    url(r'^home2.html$',
        view=HomeView.as_view(),
        name='home2'),
    url(r'^home.html$',
        view=HomeView.as_view(),
        name='home'),

    # base URL
    url(r'^$',
        MainView.as_view(),
        name='home-page'),
]
