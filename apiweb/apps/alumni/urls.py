from __future__ import unicode_literals, absolute_import, division

from django.urls import path
from .views import alumnus_list, alumnus_detail


app_name = "alumni"
urlpatterns = [
    path("", view=alumnus_list, name="alumnus-list"),
    path("alumnus/<slug>/", alumnus_detail, name="alumnus-detail"),
]
