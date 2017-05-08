from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and obj.id != model.objects.get().id):
        raise ValidationError("Errror: only 1 instance of {0} is allowed and it already exists.".format(model.__name__))

class ContactInfo(models.Model):
    secretary_email_address = models.EmailField(_("API Secretariat e-mail address"), default="secr-astro-science@uva.nl")
    address_api = models.CharField(_("API Address"), max_length=256, default="Sciencepark 904, 1098XH, Amsterdam")
    postbox_address_api = models.CharField(_("API PO Box Address"), max_length=256, default="PO Box 94249, 1090 GE Amsterdam")
    telephone_api = models.CharField(_("API Phone Number"), default="0031205257491", max_length=20)
    webmaster_email_address = models.EmailField(_("API Webmaster e-mail address"), default="secr-astro-science@uva.nl")

    class Meta:
        verbose_name = "API contact info"
        verbose_name_plural = "API contact info"

    def clean(self):
        validate_only_one_instance(self)
