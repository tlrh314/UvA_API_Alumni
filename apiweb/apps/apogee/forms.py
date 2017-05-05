from __future__ import unicode_literals, absolute_import, division

from django import forms
from .models import Entry

class EntryAdminForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data.get("date")
        date_end = cleaned_data.get("date_end")

        if date and date_end:
            # Only do something if both fields are valid so far.
            if date > date_end:
                raise forms.ValidationError(
                    "The end date of an event "
                    "should be later than the date of the event.")

        # Always return the full collection of cleaned data.
        return cleaned_data


#class EntryForm(EntryAdminForm):
class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        exclude = ('creator',)
