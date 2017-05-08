from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("secretary_email_address", "address_api", )

    ##TODO make sure there is only 1
    #def save_model(self, request, obj, form, change):
    #    contact = ContactInfo.objects.all()
    #    if contact:
    #        raise IETS WAARMEE JE MAAR 1 ding kan doen
