from __future__ import unicode_literals, absolute_import, division

from .decorators import IPAddress
from .settings import ALLOWED_IPS
from .ipaddress import IPAddress
from django.contrib.sites.models import Site


def ipaddress(request):
    """
    """

    ipaddress = IPAddress(request.META['REMOTE_ADDR'])

    return {'ipaddress': dict(
        is_allowed=ipaddress.matches(ALLOWED_IPS),
        number=ipaddress.number,
        name=ipaddress.name
        )}


def location(request):
    location = {}

    current_site = Site.objects.get_current()
    location['site'] = current_site

    script_name = request.META['SCRIPT_NAME']
    location['script_name'] = script_name

    path = request.META['PATH_INFO']
    location['path'] = path

    url = 'http://{}{}{}'.format(current_site, script_name, path)
    location['url'] = url

    return {'location': location}
