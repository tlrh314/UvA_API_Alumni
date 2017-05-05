from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import LogoView, IndexView, ObservatoryView, AdressesView
from .views import ShowProfileView, CreateProfileView, EditProfileView
from .phonelist import TelephonelistView

handler500 = 'apiweb.apps.main.errorview.server_error'

urlpatterns = [
    url(r'^create/$',
        view=CreateProfileView.as_view(),
        name='create-profile'),
    url(r'^edit/$',
        view=EditProfileView.as_view(),
        name='edit-profile'),
    url(r'^show/$',
        view=ShowProfileView.as_view(),
        name='show-profile'),
    url(r'^logo/$',
        view=LogoView.as_view(),
        name='logo'),
    url(r'^observatory/$',
        view=ObservatoryView.as_view(),
        name='observatory'),
    url(r'^addresses/phonelist/$',
        view=TelephonelistView.as_view(),

        name='addresses-phonelist'),
    url(r'^addresses/$',
        view=AdressesView.as_view(),
        name='addresses'),
    url(r'^show/$',
        view=ShowProfileView.as_view(),
        name='show-profile'),
    url(r'^edit/$',
        view=EditProfileView.as_view(),
        name='edit-profile'),
    url(r'^create/$',
        view=CreateProfileView.as_view(),
        name='create-profile'),
    url(r'^$',
        view=IndexView.as_view(),
        name='index'),
]
