from __future__ import absolute_import, division, unicode_literals

from django.urls import path

from .views import alumnus_detail, alumnus_list

app_name = "alumni"
urlpatterns = [
    path("", view=alumnus_list, name="alumnus-list"),
    path("alumnus/<slug>/", alumnus_detail, name="alumnus-detail"),
]
