from __future__ import unicode_literals, absolute_import, division

from django.db.models import Q
from django.db.utils import OperationalError
from django.contrib.sites.models import Site

from apiweb.apps.main.models import ContactInfo
from apiweb.apps.interviews.models import Post, Category
from apiweb.apps.research.models import Thesis
from .decorators import IPAddress
from .settings import ALLOWED_IPS
from .ipaddress import IPAddress

class ContactInfoDefault(object):
    def __init__(self):
        """ Hardcoded in case there is no ContactInfo object """
        self.secretary_email_address = "secr-astro-science@uva.nl"
        self.address_api = "Sciencepark 904, 1098XH, Amsterdam"
        self.postbox_address_api = "PO Box 94249, 1090 GE Amsterdam"
        self.telephone_api = "0031205257491"
        self.webmaster_email_address = "secr-astro-science@uva.nl"


def contactinfo(request):
    try:
        contactinfo = ContactInfo.objects.all()
        if contactinfo:
            contactinfo = contactinfo[0]
            p = contactinfo.telephone_api
        else:
            contactinfo = ContactInfoDefault()
            p = contactinfo.telephone_api
    except OperationalError as e:
        # Catch in case the database was not yet created
        contactinfo = ContactInfoDefault()
        p = contactinfo.telephone_api

    api_phonenumber_formatted = "+"+p[2:4]+" (0)"+p[4:6]+" "+p[6:9]+" "+p[9:11]+" "+p[11:13]

    return {"contactinfo": contactinfo, "api_phonenumber_formatted": api_phonenumber_formatted }


def get_latest_theses(request):
    latest_interviews = Post.objects.filter(is_published=True)

    # TODO: filter in category__name = "Interview" and is_published = True
    if latest_interviews.count() > 6:
        latest_interviews = latest_interviews[:6]

    latest_theses = Thesis.objects.filter(type="phd").order_by("-date_of_defence")[:6]

    return {"latest_interviews": latest_interviews, "latest_theses": latest_theses}


def ipaddress(request):
    """
    """

    ipaddress = IPAddress(request.META["REMOTE_ADDR"])

    return {"ipaddress": dict(
        is_allowed=ipaddress.matches(ALLOWED_IPS),
        number=ipaddress.number,
        name=ipaddress.name
        )}


def location(request):
    location = {}

    current_site = Site.objects.get_current()
    location["site"] = current_site

    script_name = request.META["SCRIPT_NAME"]
    location["script_name"] = script_name

    path = request.META["PATH_INFO"]
    location["path"] = path

    url = "http://{}{}{}".format(current_site, script_name, path)
    location["url"] = url

    return {"location": location}
