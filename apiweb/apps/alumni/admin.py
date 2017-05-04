from __future__ import unicode_literals, absolute_import, division
import copy

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django.contrib.auth.models import User

from tinymce.widgets import TinyMCE
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import CurrentPosition, Alumnus, Degree, PostdocPosition, Job
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG



class JobAdminInline(NestedStackedInline):
    model = Job
    extra = 1
    fieldsets = [
        ( "Job information", {
            "fields":
                [ "position_name", "current_job", "company_name", "start_date",
                "stop_date", "inside_academia", "location_job" ]
            }
        )
    ]


class DegreeAdminInline(NestedStackedInline):
    extra = 1
    model = Degree
    filter_horizontal = ("thesis_advisor", )


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ("get_alumnus", )
    filter_horizontal = ( "thesis_advisor", )

    fieldsets = [
        ( "Degree Information", {
            "fields":
                [ "alumnus", "type", "date_start", "date_stop" ]
            }
        ), ( "Thesis Information", {
            "fields":
                [ "thesis_title", "date_of_defence", "thesis_url", "thesis_slug", "thesis_in_library" ]
            }
        ), ( "Extra information", {
                "classes": ["collapse"],
                "fields": ["comments"]
            }
        ),
    ]


    def get_alumnus(self, obj):
        return obj.alumnus.full_name
    get_alumnus.short_description = "Alumnus"


class PostdocPositionAdminInline(NestedStackedInline):
    model = PostdocPosition
    max_num = 1

    # fieldsets = [
    # ("Job information",
    #     {"fields":["position_name", "current_job", "company_name", "start_date", "stop_date", "inside_academia", "location_job"]}
    #     )
    # ]

class UserRawIdWidget(widgets.ForeignKeyRawIdWidget):
    """ Class to replace alumnus.user from dropdown to pk /w filter """
    def url_parameters(self):
        res = super(UserRawIdWidget, self).url_parameters()
        object = self.attrs.get("object", None)
        if object:
            res["username__exact"] = object.user.username
        return res


class AlumnusAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Init is only defined to for UserRawIdWidget """
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        if obj and obj.pk is not None:
            self.fields["user"].widget = UserRawIdWidget(
                rel=obj._meta.get_field("user").rel,
                admin_site=admin.site,
                # Pass the object to attrs
                attrs={"object": obj}
            )

    # Change biography to TinyMCE field
    look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    look["width"] = ""
    look["height"] = "200"
    biography = forms.CharField(widget=TinyMCE(mce_attrs=look))

    class Meta:
        fields = "__all__"
        model = Alumnus


@admin.register(Alumnus)
class AlumnusAdmin(NestedModelAdmin):
    list_filter = ("show_person", "current_position")
    list_display = ("user", "email", "show_person", "first_name", "prefix", "last_name")
    search_fields = ("first_name", "last_name")
    ordering = ("user__username", )
    inlines = (JobAdminInline, DegreeAdminInline, PostdocPositionAdminInline)
    # exclude = ("jobs", )

    form = AlumnusAdminForm
    filter_horizontal = ("research", "contact", )


    fieldsets = [
        ("Account information",
                {
                "fields": ["user", "show_person"]
                }),

        ("Personal information", {
                 "fields": ["first_name", "prefix", "last_name",
                             "title", "initials", "gender", "birth_date",
                             "place_of_birth", "nationality", "mugshot",
                             "photo", "biography"]
                }),

        ("Contact information", {
                "fields":["linkedin", "facebook", "email", "home_phone",
                          "homepage", "mobile"]
                }),

        ("Adress information", {
                "fields": ["address", "streetname", "streetnumber", "zipcode",
                           "city", "country"]
                }),

        ("Current Position", {
                 "fields": ["current_position", "office", "work_phone",
                             "ads_name", "research", "contact"]
                }),

        ("Extra information", {
                "classes": ["collapse"],
                "fields": ["comments"]
                }),
    ]

    class Media:
        js = ADMIN_MEDIA_JS


admin.site.register(CurrentPosition)
admin.site.register(PostdocPosition)
admin.site.register(Job)
