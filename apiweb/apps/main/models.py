from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContactInfo(models.Model):
	secretary_email_adres = models.EmailField(_('Secretary mail adres of the API'), default='secr-astro-science@uva.nl')
	adres_api = models.CharField(_('Adres of the API institute'), max_length=256, default='Sciencepark 904, 1098XH, Amsterdam')
	postbox_adres_api = models.CharField(_('Postbox adres of the API institute'),max_length=256, default='PO Box 94249, 1090 GE Amsterdam')
	telephone_api = models.CharField(_('Telephone number of the API'), default='0031205257491', max_length=20)
	webmaster_email_adres = models.EmailField(_('Webmaster mail adres'),default='secr-astro-science@uva.nl')

	class Meta:
		verbose_name = 'API contact info'
		verbose_name_plural = 'API contact info'
