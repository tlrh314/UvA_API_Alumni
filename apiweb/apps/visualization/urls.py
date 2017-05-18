from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import tree, tree2


urlpatterns = [
    url(r"^tree$", view=tree, name="tree"),
    url(r"^tree2$", view=tree2, name="tree2"),
]

