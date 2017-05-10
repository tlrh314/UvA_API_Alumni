from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import tree


urlpatterns = [
    url(r"^tree$", view=tree, name="tree"),
]

