from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import thesis_list, thesis_detail, thesis_has_no_pdf


urlpatterns = [
    url(r"^$", view=thesis_list, name="thesis-list"),
    url(r"^(?P<slug>.*)/$", thesis_detail, name="thesis-detail"),
    url(r"^thesis_not_found$", thesis_has_no_pdf, name="thesis-has-no-pdf"),
]
