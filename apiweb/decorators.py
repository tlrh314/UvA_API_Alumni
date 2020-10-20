from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from .ipaddress import IPAddress
from .settings import ALLOWED_IPS, TEMPLATE403


def protect_by_ip(function):
    def decorator(request, *args, **kwargs):
        try:
            ipaddress = IPAddress(request.META["HTTP_X_FORWARDED_FOR"])
        except KeyError:
            ipaddress = IPAddress(request.META["REMOTE_ADDR"])
        if ipaddress.matches(ALLOWED_IPS) is False:
            raise Http404()
        return function(request, *args, **kwargs)

    return decorator


def ipallowed_or_403(function):
    def decorator(request, *args, **kwargs):
        try:
            ipaddress = IPAddress(request.META["HTTP_X_FORWARDED_FOR"])
        except KeyError:
            ipaddress = IPAddress(request.META["REMOTE_ADDR"])
        if ipaddress.matches(ALLOWED_IPS) is False:
            response = render_to_response(
                TEMPLATE403, context_instance=RequestContext(request)
            )
            response.status_code = 403
            return response
        return function(request, *args, **kwargs)

    return decorator
