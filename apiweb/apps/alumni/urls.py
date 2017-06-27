from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import alumnus_list, alumnus_detail


urlpatterns = [
    url(r"^$", view=alumnus_list, name="alumnus-list"),
    url(r"alumnus/(?P<slug>.*)/$", alumnus_detail, name="alumnus-detail"),
]
