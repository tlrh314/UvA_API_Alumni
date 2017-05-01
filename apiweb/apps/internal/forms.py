from __future__ import unicode_literals, absolute_import, division

import django.contrib.auth.forms
from django import forms
from django.utils.translation import ugettext as _


class PasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):

    old_password = forms.CharField(
        label=_("Old password"), widget=forms.PasswordInput(
            attrs={'autofocus': 'autofocus'}))


class LoginForm(django.contrib.auth.forms.AuthenticationForm):

    username = forms.CharField(
        label=_("Username"), max_length=50,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
