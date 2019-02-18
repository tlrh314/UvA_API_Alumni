from __future__ import unicode_literals, absolute_import, division

from django.urls import path
# from .views import SearchView
from .views import search
# handler500 = 'apiweb.apps.main.errorview.server_error'

app_name = "search"
urlpatterns = [
    # path(r'', view=SearchView.as_view(), name='index'),
    path(r'', view=search, name='search'),
]
