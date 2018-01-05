from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from .views import tree
from .views import view_a, view_b, view_c, view_d, view_e, view_f


urlpatterns = [
    url(r"^student_supervisor_tree$", view=tree, name="tree"),
    url(r"^in_astronomy$", view=view_a, name="view_a"),
    url(r"^job_location$", view=view_b, name="view_b"),
#    url(r"^c$", view=view_c, name="view_c"),
    url(r"^job_sector$", view=view_d, name="view_d"),
    url(r"^land_of_origin$", view=view_e, name="view_e"),
    url(r"^alumni_gender$", view=view_f, name="view_f"),
]

