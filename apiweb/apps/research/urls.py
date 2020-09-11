from django.urls import path

from .views import thesis_detail, thesis_has_no_pdf, thesis_list

app_name = "research"
urlpatterns = [
    path("", view=thesis_list, name="thesis-list"),
    path("<slug>", thesis_detail, name="thesis-detail"),
    path("thesis_not_found", thesis_has_no_pdf, name="thesis-has-no-pdf"),
]
