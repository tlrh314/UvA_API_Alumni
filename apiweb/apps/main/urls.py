from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import include, url
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from apiweb.context_processors import contactinfo
from .views import index, contact, contact_success, privacy_policy
from .views import site_contactinfo, site_privacysettings


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^thanks/$', contact_success, name='contact_success'),
    url(r'^privacy-policy/$', privacy_policy, name='privacy_policy'),

    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='main/login.html'
        ), name="site_login"
    ),
    url(r'^logout/$', auth_views.LogoutView.as_view(
        template_name='main/logged_out.html'
        ), name='site_logout'
    ),

    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(
        template_name='main/password_change_form.html',
        success_url = reverse_lazy('site_password_change_done')
        ), name='site_password_change'
    ),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='main/password_change_done.html',
        ), name='site_password_change_done'
    ),

    url(r"^contactinfo/$", site_contactinfo, name="site_contactinfo"),
    url(r"^privacysettings/$", site_privacysettings, name="site_privacysettings"),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(
            template_name='main/password_reset_form.html',
            extra_context = {
                "api_phonenumber_formatted": contactinfo(None)["api_phonenumber_formatted"],
                "secretary_email_address": contactinfo(None)["contactinfo"].secretary_email_address,
            },
            email_template_name='main/password_reset_email.html',
            extra_email_context = {
                "api_phonenumber_formatted": contactinfo(None)["api_phonenumber_formatted"],
                "secretary_email_address": contactinfo(None)["contactinfo"].secretary_email_address,
            },
            success_url = reverse_lazy('site_password_reset_done')
        ), name='site_password_reset'
    ),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(
            template_name='main/password_reset_done.html',
            extra_context = {
                "api_phonenumber_formatted": contactinfo(None)["api_phonenumber_formatted"],
                "secretary_email_address": contactinfo(None)["contactinfo"].secretary_email_address,
            },
        ), name='site_password_reset_done'
    ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='main/password_reset_confirm.html',
            success_url = reverse_lazy('site_password_reset_complete')
        ), name='site_password_reset_confirm'
    ),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='main/password_reset_complete.html'
        ), name='site_password_reset_complete'
    ),
]
