from __future__ import absolute_import, division, unicode_literals

from django.urls import path

from .views import tree, view_a, view_b, view_c, view_d, view_e, view_f

app_name = "visualization"
urlpatterns = [
    path("student_supervisor_tree", view=tree, name="tree"),
    path("in_astronomy", view=view_a, name="view_a"),
    path("job_location", view=view_b, name="view_b"),
    #    path(r"c", view=view_c, name="view_c"),
    path("job_sector", view=view_d, name="view_d"),
    path("land_of_origin", view=view_e, name="view_e"),
    path("alumni_gender", view=view_f, name="view_f"),
]
