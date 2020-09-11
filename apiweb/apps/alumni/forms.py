import copy

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE

from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG
from .models import Alumnus, PreviousPosition


class PreviousPositionAdminForm(forms.ModelForm):
    nova = forms.MultipleChoiceField(
        widget=forms.RadioSelect(), choices=PreviousPosition.NOVA_NETWORK
    )
    # Remove following line for dropdown.
    funding = forms.MultipleChoiceField(
        widget=forms.RadioSelect(), choices=PreviousPosition.FUNDING
    )


class AlumnusAdminForm(UserChangeForm):
    # Change biography to TinyMCE field
    look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    look["width"] = ""
    look["height"] = "200"
    biography = forms.CharField(required=False, widget=TinyMCE(mce_attrs=look))

    class Meta:
        fields = "__all__"
        model = Alumnus

    username = forms.CharField(
        required=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and ./+/-/_ only."
        ),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        required=False,
        help_text="Your email address will also serve as a way to log in",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data.get("username")
        if "@" in username:
            self._errors["username"] = ErrorList()
            self._errors["username"].append("The username cannot contain '@'.")

        initials = self.cleaned_data.get("initials")
        if any(str.isdigit(c) for c in initials):
            self._errors["initials"] = ErrorList()
            self._errors["initials"].append("Initials cannot contain numbers")
        if "." in initials:
            self._errors["initials"] = ErrorList()
            self._errors["initials"].append(
                "Please give initials without dots, letters only"
            )

        first_name = self.cleaned_data.get("first_name")
        if any(str.isdigit(c) for c in first_name):
            self._errors["first_name"] = ErrorList()
            self._errors["first_name"].append("First names cannot contain numbers")

        prefix = self.cleaned_data.get("prefix")
        if any(str.isdigit(c) for c in prefix):
            self._errors["prefix"] = ErrorList()
            self._errors["prefix"].append("Prefixes cannot contain numbers")

        # As last name is already required, we cannot just override this stuff. So lets' ''try''
        last_name = self.cleaned_data.get("last_name")
        if last_name and any(str.isdigit(c) for c in last_name):
            self._errors["last_name"] = ErrorList()
            self._errors["last_name"].append("Last names cannot contain numbers")

        place_of_birth = self.cleaned_data.get("place_of_birth")
        if any(str.isdigit(c) for c in place_of_birth):
            self._errors["place_of_birth"] = ErrorList()
            self._errors["place_of_birth"].append(
                "Places of birth cannot contain numbers"
            )

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

        # Because there is also a possibility to log in with email, one must not use an email which is already in use.
        # TODO: if the user has an email, but the form is empty, that means that the person wants to remove the data, but this way wouldt let it
        # SO make a check whether there is instance data but form data is empty

        email = self.cleaned_data.get("email")
        if email:

            # Remove this instance object from duplicate emails object list
            duplicate_emails_excluded = Alumnus.objects.filter(email=email).exclude(
                pk=self.instance.pk
            )
            # TODO: Change len() to .count()
            if len(duplicate_emails_excluded) > 0:
                self.errors["email"] = ErrorList()
                self.errors["email"].append("The chosen email address is already used")


# ##NEW USERFORM TEST
UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update(
                {"autofocus": True}
            )

    def clean_email(self):
        super().clean()
        email = self.cleaned_data.get("email")
        duplicate_emails = Alumnus.objects.filter(email=email)
        if len(duplicate_emails) > 0:
            self.errors["email"] = ErrorList()
            self.errors["email"].append("The chosen email address is already used")
        return email
