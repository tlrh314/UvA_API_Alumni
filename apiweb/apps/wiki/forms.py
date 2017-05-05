from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import WikiPage


class WikiPageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 70, 'rows': 40, 'autofocus': 'autofocus'}))

    class Meta:
        model = WikiPage
        fields = ['text']


class WikiPageCreateForm(forms.Form):
    name = forms.SlugField(label=_('Page name'), max_length=256,
                           widget=forms.TextInput(
                               attrs={'autofocus': 'autofocus'}))
    is_category_page = forms.BooleanField(label=_('Page is a category page'),
                                          required=False)
