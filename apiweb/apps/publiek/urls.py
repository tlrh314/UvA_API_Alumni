from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import StudieView, LinksView, EducatieView, PubliekView
from .views import StarnightsView, ApplicationFormView, ThanksView
from .views import OnderzoekView, PlanetsView, StarsView, LiveView
from .views import ExplosionsView, AccretionView, CompactsView, ExtremeView

handler500 = 'apiweb.main.errorview.server_error'


urlpatterns = [
    url(r'^sterrenkijkavonden/$',
        view=StarnightsView.as_view(),
        name='sterrenkijkavonden'),
    url(r'^aanmeldingsformulier/$',
        view=ApplicationFormView.as_view(),
        name='aanmeldingsformulier'),
    url(r'^thanks/$',
        view=ThanksView.as_view(),
        name='thanks'),
    url(r'^educatie/$',
        view=EducatieView.as_view(),
        name='educatie'),
    url(r'^studie/$',
        view=StudieView.as_view(),
        name='studie'),
    url(r'^links/$',
        view=LinksView.as_view(),
        name='links'),
    url(r'^onderzoek/live/planets/$',
        view=PlanetsView.as_view(),
        name='planets'),
    url(r'^onderzoek/live/stars/$',
        view=StarsView.as_view(),
        name='stars'),
    url(r'^onderzoek/live/$',
        view=LiveView.as_view(),
        name='live'),
    url(r'^onderzoek/extreme/explosions/$',
        view=ExplosionsView.as_view(),
        name='explosions'),
    url(r'^onderzoek/extreme/accretion/$',
        view=AccretionView.as_view(),
        name='accretion'),
    url(r'^onderzoek/extreme/compacts/$',
        view=CompactsView.as_view(),
        name='compacts'),
    url(r'^onderzoek/extreme/$',
        view=ExtremeView.as_view(),
        name='extreme'),
    url(r'^onderzoek/$',
        view=OnderzoekView.as_view(),
        name='onderzoek'),
    url(r'^$',
        view=PubliekView.as_view(),
        name='index'),
]
