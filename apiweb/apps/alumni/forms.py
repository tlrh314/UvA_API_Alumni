import copy

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.forms.utils import ErrorList

from tinymce.widgets import TinyMCE
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField


from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG
from .models import PreviousPosition, Alumnus


class PreviousPositionAdminForm(forms.ModelForm):
    nova = forms.MultipleChoiceField(widget=forms.RadioSelect(), choices=PreviousPosition.NOVA_NETWORK)
    # Remove following line for dropdown.
    funding = forms.MultipleChoiceField(widget=forms.RadioSelect(), choices=PreviousPosition.FUNDING)


class AlumnusAdminForm(forms.ModelForm):
    # Change biography to TinyMCE field
    look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    look["width"] = ""
    look["height"] = "200"
    biography = forms.CharField(required=False, widget=TinyMCE(mce_attrs=look))

    class Meta:
        fields = "__all__"
        model = Alumnus


    def clean(self):
        initials = self.cleaned_data.get("initials")
        if any(str.isdigit(c) for c in initials):
            self._errors["initials"] = ErrorList()
            self._errors["initials"].append("Initials cannot contain numbers")
        if "." in initials:
            self._errors["initials"] = ErrorList()
            self._errors["initials"].append("Please give initials without dots, letters only")

        first_name = self.cleaned_data.get("first_name")
        if any(str.isdigit(c) for c in first_name):
            self._errors["first_name"] = ErrorList()
            self._errors["first_name"].append("First names cannot contain numbers")

        prefix = self.cleaned_data.get("prefix")
        if any(str.isdigit(c) for c in prefix):
            self._errors["prefix"] = ErrorList()
            self._errors["prefix"].append("Prefixes cannot contain numbers")

        #As last name is already required, we cannot just override this stuff. So lets' ''try''
        last_name = self.cleaned_data.get("last_name")
        if last_name and any(str.isdigit(c) for c in last_name):
                self._errors["last_name"] = ErrorList()
                self._errors["last_name"].append("Last names cannot contain numbers")

        place_of_birth = self.cleaned_data.get("place_of_birth")
        if any(str.isdigit(c) for c in place_of_birth):
            self._errors["place_of_birth"] = ErrorList()
            self._errors["place_of_birth"].append("Places of birth cannot contain numbers")

        mobile = self.cleaned_data.get("mobile")
        if mobile and not any(str.isdigit(c) for c in mobile):
            self._errors["mobile"] = ErrorList()
            self._errors["mobile"].append("Phone numbers can only contain numbers")

        home_phone = self.cleaned_data.get("home_phone")
        if home_phone and not any(str.isdigit(c) for c in home_phone):
            self._errors["home_phone"] = ErrorList()
            self._errors["home_phone"].append("Phone numbers can only contain numbers")

        work_phone = self.cleaned_data.get("work_phone")
        if work_phone and not any(str.isdigit(c) for c in work_phone):
            self._errors["work_phone"] = ErrorList()
            self._errors["work_phone"].append("Phone numbers can only contain numbers")

