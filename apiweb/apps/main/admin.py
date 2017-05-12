from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import ContactInfo
from .models import WelcomeMessage


@admin.register(WelcomeMessage)
class WelcomeMessageAdmin(admin.ModelAdmin):
    list_display = ("rename_text",)

    def rename_text(self, obj):
       return "Click here to change the Welcome Message"
    rename_text.short_description = "Welcome Message"


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = "__all__"

    def clean(self):
        phonenumber = self.cleaned_data.get("telephone_api")

        if len(phonenumber) != 13 and phonenumber[0:4] != "003120":
            raise forms.ValidationError("Please enter 13 digits for the phone number, starting with 003120")
        return self.cleaned_data


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("secretary_email_address", "webmaster_email_address",
                    "postbox_address_api", "address_api", "telephone_api" )
    form = ContactInfoForm
