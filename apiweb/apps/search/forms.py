from __future__ import absolute_import, division, unicode_literals

from django import forms


class SearchForm(forms.Form):
    search_terms = forms.CharField(
        label="Search", required=True, widget=forms.TextInput(attrs={"size": 60})
    )
