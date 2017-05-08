from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("secretary_email_address", "webmaster_email_address",
                    "postbox_address_api", "address_api", "telephone_api" )
