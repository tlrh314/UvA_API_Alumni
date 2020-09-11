from django.core.files.storage import FileSystemStorage
from filebrowser.sites import site

from .base import *

site.storage = FileSystemStorage(location=STATIC_ROOT, base_url=STATIC_URL)
site.directory = "img/"
