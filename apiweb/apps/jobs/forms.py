from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.utils.translation import ugettext as _
from .models import Job


class JobAdminForm(forms.ModelForm):
    teaser = forms.CharField(
        label=_("Teaser text"), widget=forms.Textarea(attrs={
            'cols': 80, 'rows': 3}),
        required=True)

    class Meta:
        model = Job
        fields = '__all__'
