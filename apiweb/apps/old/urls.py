from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from django.views.generic import TemplateView

handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^main.html$',
        view=TemplateView.as_view(template_name='old/main.html'),
        name='main'),
    url(r'^top.html$',
        view=TemplateView.as_view(template_name='old/top.html'),
        name='top'),
    url(r'^navigation.html$',
        view=TemplateView.as_view(template_name='old/navigation.html'),
        name='navigation'),
    url(r'^$',
        view=TemplateView.as_view(template_name='old/home.html'),
        name='index'),
]
