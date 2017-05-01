from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
import django.contrib.auth.views
from .forms import PasswordChangeForm, LoginForm

handler500 = 'apiweb.main.errorview.server_error'

# Deze views in auth zijn nog niet class-based

urlpatterns = [
    url(r'^login/$',
        view=django.contrib.auth.views.login,
        kwargs={'template_name': 'internal/login_form.html',
                'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$',
        view=django.contrib.auth.views.logout,
        kwargs={'template_name': 'internal/logged_out.html'},
        name='logout'),
    url(r'^password_change/$',
        view=django.contrib.auth.views.password_change,
        kwargs={
            'template_name': 'internal/password_change_form.html',
            'password_change_form': PasswordChangeForm,
            # Semi-hack, because auth doesn't work nice with namespaces
            'post_change_redirect': '/internal/account/password_change_done'},
        name='password-change'),
    url(r'^password_change_done/$',
        view=django.contrib.auth.views.password_change_done,
        kwargs={'template_name': 'internal/password_change_done.html'},
        name='password-change-done'),
]
