from __future__ import unicode_literals, absolute_import, division

from django.urls import path
from .views import tree
from .views import view_a, view_b, view_c, view_d, view_e, view_f


app_name = "visualization"
urlpatterns = [
    path(r"student_supervisor_tree", view=tree, name="tree"),
    path(r"in_astronomy", view=view_a, name="view_a"),
    path(r"job_location", view=view_b, name="view_b"),
#    path(r"c", view=view_c, name="view_c"),
    path(r"job_sector", view=view_d, name="view_d"),
    path(r"land_of_origin", view=view_e, name="view_e"),
    path(r"alumni_gender", view=view_f, name="view_f"),
]

