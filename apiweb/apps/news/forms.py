from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.utils.translation import ugettext as _
from .models import Press, Event, Colloquium, Pizza


class PressAdminForm(forms.ModelForm):
    teaser_text = forms.CharField(
        label=_("Teaser text"), widget=forms.Textarea(attrs={
            'cols': 80, 'rows': 3}),
        required=False)

    class Meta:
        model = Press
        fields = '__all__'


class EventAdminForm(forms.ModelForm):
    teaser_text = forms.CharField(
        label=_("Teaser text"), widget=forms.Textarea(attrs={
            'cols': 80, 'rows': 3}),
        required=False)

    class Meta:
        model = Event
        fields = '__all__'


class ColloquiumAdminForm(forms.ModelForm):
    text = forms.CharField(label=_("Abstract"), widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 12}), required=False)
    teaser_text = forms.CharField(
        label=_("Teaser text"), widget=forms.Textarea(attrs={
            'cols': 80, 'rows': 3}),
        required=False)

    def clean(self):
        try:
            if self.cleaned_data['date_off'] and self.cleaned_data['date_on']:
                if self.cleaned_data['date_off'] < self.cleaned_data['date_on']:
                    self._errors['date_off'] = forms.utils.ErrorList([""])
                    self._errors['date_on'] = forms.utils.ErrorList([""])
                    del self.cleaned_data['date_off']
                    del self.cleaned_data['date_on']
                    raise forms.ValidationError(
                        "'Date off' is before 'date on'")
        # missing date_off or date_on; let default cleaning handle that
        except KeyError:
            pass
        super(ColloquiumAdminForm, self).clean()
        return self.cleaned_data

    class Meta:
        model = Colloquium
        fields = '__all__'


class PizzaAdminForm(forms.ModelForm):
    text = forms.CharField(label=_("Abstract"), widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 12}), required=False)
    teaser_text = forms.CharField(
        label=_("Teaser text"), widget=forms.Textarea(attrs={
            'cols': 80, 'rows': 3}),
        required=False,
        help_text=_("one or two short sentences for on the front webpage"))

    def clean(self):
        try:
            if self.cleaned_data['date_off'] and self.cleaned_data['date_on']:
                if self.cleaned_data['date_off'] < self.cleaned_data['date_on']:
                    self._errors['date_off'] = forms.utils.ErrorList([""])
                    self._errors['date_on'] = forms.utils.ErrorList([""])
                    del self.cleaned_data['date_off']
                    del self.cleaned_data['date_on']
                    raise forms.ValidationError(
                        "'Date off' is before 'date on'")
        # missing date_off or date_on; let default cleaning handle that
        except KeyError:
            pass
        super(PizzaAdminForm, self).clean()
        return self.cleaned_data

    class Meta:
        model = Pizza
        fields = '__all__'
