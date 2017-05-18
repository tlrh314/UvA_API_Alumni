# Extra default settings, that should follow after the local settings, and thus can't be set in base.

import os.path
from . import BASE_DIR, MEDIA_ROOT, STATIC_ROOT, MEDIA_URL, STATIC_URL

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


CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = False


# TODO: cities_light might have ajax-lookupable countries
AJAX_LOOKUP_CHANNELS = {
#    'cities_light_country': ('cities_light.lookups', 'CountryLookup'),
#    'cities_light_city': ('cities_light.lookups', 'CityLookup'),
    'user': {'model':'auth.user','search_field':'username'}
}
#
# CITIES_LIGHT_TRANSLATION_LANGUAGES = ['fr', 'en']
# CITIES_LIGHT_INCLUDE_COUNTRIES = ['FR']
# CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC',
#     'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]
