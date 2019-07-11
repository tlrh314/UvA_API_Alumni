#!/srv/api/venv/bin/python
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, 'src')))
sys.path.insert(0, os.path.abspath('/srv/apiweb/venv3/lib/python3.7/site-packages/'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'apiweb.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
