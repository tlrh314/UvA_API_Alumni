# Django settings for api project.

# Make a copy of local_template.py to local.py and edit that copy,
# filling in all the undefined values (or changing them accordingly).


import os.path

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

MIDDLEWARE_CLASSES = (
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

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'apiweb.apps.people',
    'apiweb.apps.research',

    # 'nested_inline',
    'apiweb.apps.main',
    'apiweb.apps.search',
    'apiweb.apps.alumni',
    'apiweb.apps.survey',
    'apiweb.apps.interviews',
    'apiweb.apps.visualization',

    'bootstrap3',
    'django_countries',
    'crispy_forms',
    # 'cities_light',
)

# login URL for auth app
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/redirect_to_profile'
#AUTH_USER_MODEL = 'alumni.Alumnus'

NEWS_LANGUAGES = ('en', 'nl')
#NEWS_LANGUAGES = ('en',)  # 'nl')

TEMPLATE403 = '403.html'
