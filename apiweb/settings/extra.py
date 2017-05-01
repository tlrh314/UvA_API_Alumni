# Extra default settings, that should follow after the local settings, and thus can't be set in base.

import os.path
from . import BASE_DIR, MEDIA_ROOT, STATIC_ROOT, MEDIA_URL, STATIC_URL

STAFF_MEDIA_URL = MEDIA_URL + 'uploads/staff_meetings'
STAFF_MEDIA_ROOT = os.path.join(MEDIA_ROOT, '/uploads/staff_meetings/')

ADMIN_MEDIA_JS = (
    STATIC_URL + 'javascript/jquery.js',
    STATIC_URL + 'javascript/tinymce/tinymce.min.js',
    STATIC_URL + 'javascript/admin/tinymce_setup.js',
)

FILEBROWSER_SHOW_IN_DASHBOARD = True

