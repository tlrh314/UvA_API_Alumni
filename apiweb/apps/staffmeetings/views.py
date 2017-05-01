from __future__ import unicode_literals, absolute_import, division

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.http import http_date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from wsgiref.util import FileWrapper
from ...settings import STAFF_MEDIA_ROOT
from .models import Staffmeeting

import mimetypes
import os
import posixpath
import stat
import urllib
import time


class IndexView(ListView):

    template_name = 'staffmeetings/staffmeeting_list.html'
    model = Staffmeeting

    def get_queryset(self):
        queryset = self.model.objects.filter(date__year=self.year).order_by(
            '-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        can_view = self.request.user.groups.filter(
            name__in=["staff", "secretariat"])
        title = 'Staff meetings at the Anton Pannekoek Institute'

        context['year'] = self.year
        context['title'] = title
        context['staff'] = can_view
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        year = kwargs.get('year', None)
        self.year = int(year) if year is not None else time.localtime()[0]
        # or year = datetime.datetime.now().year
        return super(IndexView, self).dispatch(*args, **kwargs)


class CheckFileView(View):

    def dispatch(self, request, *args, **kwargs):
        path = kwargs.get('path', None)
        if not request.user.is_authenticated():
            raise Http404
        if '/private/' in path:
            if not request.user.groups.filter(
                    name__in=('staff', 'secretariat')):
                raise Http404
        # Clean up given path to only allow serving files below document_root.
        path = posixpath.normpath(urllib.unquote(path))
        path = path.lstrip('/')
        newpath = ''
        for part in path.split('/'):
            if not part:
                # Strip empty path components.
                continue
            _, part = os.path.splitdrive(part)
            _, part = os.path.split(part)
            if part in (os.curdir, os.pardir):
                # Strip '.' and '..' in path.
                continue
            newpath = os.path.join(newpath, part).replace('\\', '/')
        if newpath and path != newpath:
            return HttpResponseRedirect(newpath)
        fullpath = os.path.join(STAFF_MEDIA_ROOT, newpath)
        if os.path.isdir(fullpath):
            raise Http404
        if not os.path.exists(fullpath):
            raise Http404
        statobj = os.stat(fullpath)
        mimetype = (mimetypes.guess_type(fullpath)[0] or
                    'application/octet-stream')
#
# file in one chunk
#       contents = open(fullpath, 'rb').read()
# file in chunks of 8 KB
        contents = FileWrapper(file(fullpath))
#
        response = HttpResponse(contents, content_type=mimetype)
        response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
#
# file in one chunk
#       response["Content-Length"] = len(contents)
# file in chunks of 8 KB
        response["Content-Length"] = os.path.getsize(fullpath)
#
        return response
