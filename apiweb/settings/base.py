import os
import os.path
import logging
import environ
from logging import handlers

env = environ.Env()
env.read_env(
    str((environ.Path(__file__) - 1).path(".env"))
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
#USE_TZ = True
USE_TZ = False


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = '/media/'


# URL that handles the media served from STATIC_ROOT. Make sure to use a
# trailing slash.
STATIC_URL = '/static/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
)

# CommonMiddleware settings
APPEND_SLASH = True
#PREPEND_WWW = True


ROOT_URLCONF = 'apiweb.urls'


# ensure large uploaded files end up with correct permissions. See
# http://docs.djangoproject.com/en/dev/ref/settings/#file-upload-permissions
FILE_UPLOAD_PERMISSIONS = 0o664


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apiweb.context_processors.ipaddress',
                'apiweb.context_processors.location',
                'apiweb.context_processors.contactinfo',
                'apiweb.context_processors.get_latest_theses',
            ],
            # Leave out 'loaders' to use the default template loaders
            # Leave out 'debug' to use the same as DEBUG
        },
    },
]


INSTALLED_APPS = (
    #Filebrowser should be listed before django.contrib.admin
    'tinymce',
    'ajax_select',
    'filebrowser',
    'dal',
    'dal_select2',

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'apiweb.apps.main',
    'apiweb.apps.search',
    'apiweb.apps.alumni',
    'apiweb.apps.research',
    'apiweb.apps.survey',
    'apiweb.apps.interviews',
    'apiweb.apps.visualization',

    'bootstrap3',
    'django_countries',
    'crispy_forms',
)

# login URL for auth app
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/redirect_to_profile'
AUTH_USER_MODEL = 'alumni.Alumnus'
AUTHENTICATION_BACKENDS = [
    'apiweb.apps.alumni.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
]


NEWS_LANGUAGES = ('en', 'nl')
#NEWS_LANGUAGES = ('en',)  # 'nl')

TEMPLATE403 = '403.html'

# `env LC_CTYPE=C tr -dc "a-zA-Z0-9" < /dev/random | head -c 50; echo`
SECRET_KEY = env('SECRET_KEY', default='secret')


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ADMINS = (('Admin Naam', 'Admin@emailaddress.com'),
#           ('Admin2 Naam', 'Admin2@emailaddress.com'),)
#
# MANAGERS = ADMINS
SENTRY_DSN_API = env('SENTRY_DSN_API', default='')
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
sentry_sdk.init(
    dsn=SENTRY_DSN_API,
    integrations=[DjangoIntegration()],
    environment=env('SENTRY_ENVIRONMENT', default='development')
)


DEBUG = env("DEBUG", default=False)
SEND_BROKEN_LINK_EMAILS = True

EMAIL_CONFIG = env.email_url("EMAIL_URL")
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = "no-reply@api-alumni.nl"
SERVER_EMAIL = "no-reply@api-alumni.nl"

GOOGLE_API_KEY = env('GOOGLE_API_KEY')
GOOGLE_CX_ID env('GOOGLE_CX_ID')

FLICKR_APIKEY = env('FLICKR_APIKEY')
FLICKR_USERID = env('FLICKR_USERID')
FLICKR_SECRET = env('FLICKR_SECRET')
FLICKR_TOKEN_PATH = os.path.join(BASE_DIR, 'databases', 'flickr')


DATABASES = {
    'default':  env.db('DATABASE_DEFAULT'),
    # 'wiki':  env.db('DATABASE_WIKI'),
}
if "mysql" in DATABASES["default"]["ENGINE"]:
    if not DATABASES["default"]["OPTIONS"]:
        DATABASES["default"]["OPTIONS"] = dict()
    DATABASES["default"]["OPTIONS"]["init_command"] = "SET foreign_key_checks = 0;"
DATABASE_ROUTERS = [
    'apiweb.dbrouters.WikiRouter',
    'apiweb.dbrouters.DefaultRouter'
]


ALLOWED_HOSTS = ['*']
ALLOWED_IPS = ['allowed-ips']


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Amsterdam'
DATE_FORMAT = 'j-n-Y'
DATETIME_FORMAT = 'j-n-Y H:i'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'staticfiles'),
)


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'apiweb.server.wsgi.application'


class GroupWriteRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """ https://stackoverflow.com/questions/1407474 """
    def _open(self):
        prevumask = os.umask(0o002)
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(module)s'+\
                    '%(name)s %(process)d %(thread)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'survey': {
            'level': 'DEBUG',
            'class': 'apiweb.settings.GroupWriteRotatingFileHandler',
            'filename': 'log/survey.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'survey': {
            'handlers': ['survey'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


STAFF_MEDIA_URL = MEDIA_URL + 'uploads/staff_meetings'
STAFF_MEDIA_ROOT = os.path.join(MEDIA_ROOT, '/uploads/staff_meetings/')

ADMIN_MEDIA_JS = (
    (STATIC_URL + 'js/action_buttons.js', )
)

FILEBROWSER_SHOW_IN_DASHBOARD = True
FILEBROWSER_DEFAULT_PERMISSIONS = 0o644
FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Document': [], # ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Video': [], # ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    'Audio': [], # ['.mp3','.mp4','.wav','.aiff','.midi','.m4p']
}
FILEBROWSER_ADMIN_VERSIONS = ['big'] # 'thumbnail', 'small', 'medium', 'large'

# TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_FILEBROWSER = True
# https://www.tinymce.com/docs/demo/full-featured/
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'height': 500,
    'theme': 'modern',
    'plugins': [
        'advlist autolink lists link image charmap print preview hr anchor pagebreak',
        'searchreplace wordcount visualblocks visualchars code fullscreen',
        'insertdatetime media nonbreaking save table contextmenu directionality',
        'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'
    ],
    'toolbar1': 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
    'toolbar2': 'print preview image | forecolor backcolor emoticons | codesample',
    'image_advtab': True,
    'templates': [
        { 'title': 'Test template 1', 'content': 'Test 1' },
        { 'title': 'Test template 2', 'content': 'Test 2' }
    ],
    'paste_as_text': True,
    'content_css': [
    ],
}
TINYMCE_MINIMAL_CONFIG = {
    'selector': 'textarea',
    'height': 80,
    'width': 500,
    'menubar': False,
    'statusbar': False,
    'elementpath': False,
    'plugins': [
        'link paste autolink code',
    ],
    'toolbar1': 'undo redo | bold italic | bullist numlist outdent indent | link code',
    'toolbar2': '',
    'paste_as_text': True,
}


AJAX_LOOKUP_CHANNELS = {
    'user': {'model':'auth.user','search_field':'username'}
}

# COUNTRIES_FIRST_BREAK
COUNTRIES_FIRST = ( "NL", "DE", "FR", "GB", "US")
