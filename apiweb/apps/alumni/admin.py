from __future__ import unicode_literals, absolute_import, division
import copy

from django import forms
from django.db.models import Q
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE
# from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import CurrentPosition, Alumnus, Degree, PostdocPosition, JobAfterLeaving
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG



class JobAdminInline(admin.StackedInline):
    model = JobAfterLeaving
    extra = 0
    fieldsets = [
        ( "Job information", {
            "fields":
                [ "position_name", "current_job", "company_name", "start_date",
                "stop_date", "inside_academia", "location_job" ]
            }
        )
    ]



class DegreeAdminInline(admin.StackedInline):
    extra = 0
    model = Degree
    filter_horizontal = ("thesis_advisor", )


class DegreeListFilter(admin.SimpleListFilter):
    title = _("empty thesis title")
    parameter_name = "have_title"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no",  _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "no":
            return queryset.filter(thesis_title__isnull=False).exclude(thesis_title='')

        if self.value() == "yes":
            return queryset.filter(Q(thesis_title__isnull=True) | Q(thesis_title__exact=''))


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ("get_alumnus", "type", "thesis_title" )
    list_filter = ("type", DegreeListFilter)
    search_fields = ("thesis_title", "alumnus__last_name", "alumnus__first_name")
    ordering = ("alumnus__user__username", )
    filter_horizontal = ( "thesis_advisor", )

    max_num = 2

    fieldsets = [
        ( "Degree Information", {
            "fields":
                [ "alumnus", "type", "date_start", "date_stop" ],
            }
        ), ( "Thesis Information", {
            "fields":
                [ "thesis_title", "date_of_defence", "thesis_url", "thesis_slug", "thesis_in_library" ]
            }
        ), ( "Thesis Adivior ", {
            "fields":
                [ "thesis_advisor" ]
            }
        ), ( "Extra information", {
                "classes": ["collapse"],
                "fields": ["comments"]
            }
        ),
    ]

    def get_alumnus(self, obj):
        """ We could use author instead of get_alumnus in list_display """
        return obj.alumnus.full_name
    get_alumnus.short_description = "Alumnus"


class PostdocPositionAdminInline(admin.StackedInline):
    model = PostdocPosition
    extra = 0
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

class AlumnusListFilter(admin.SimpleListFilter):
    title = _("empty email")
    parameter_name = "have_email"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no",  _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "no":
            return queryset.filter(email__isnull=False).exclude(email='')

        if self.value() == "yes":
            return queryset.filter(Q(email__isnull=True) | Q(email__exact=''))


@admin.register(Alumnus)
class AlumnusAdmin(admin.ModelAdmin):
    ordering = ("user__username", )
    search_fields = ("first_name", "last_name", "degrees__thesis_title")
    list_display = ("get_alumnus", "email", "show_person")
    list_filter = ("show_person", "current_position", AlumnusListFilter)
    inlines = (DegreeAdminInline, PostdocPositionAdminInline, JobAdminInline)
    form = AlumnusAdminForm
    filter_horizontal = ("research", "contact", )
    readonly_fields = ("get_full_name", )
    # exclude = ("jobs", )

    fieldsets = [
        ("Account information",
                {
                    "fields": ["user", "get_full_name", "last_name", "show_person"]
                }),

        ("Personal information", {
                "classes": ["collapse"],
                 "fields": ["first_name", "prefix", "last_name",
                             "title", "initials", "gender", "birth_date",
                             "place_of_birth", "nationality", "mugshot",
                             "photo", "biography"]
                }),

        ("Contact information", {
                "classes": ["collapse"],
                "fields":["linkedin", "facebook", "email", "home_phone",
                          "homepage", "mobile"]
                }),

        ("Adress information", {
                "classes": ["collapse"],
                "fields": ["address", "streetname", "streetnumber", "zipcode",
                           "city", "country"]
                }),

        ("Current Position", {
                "classes": ["collapse"],
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

    def get_alumnus(self, obj):
        """ We could use author instead of get_alumnus in list_display """
        return obj.full_name
    get_alumnus.short_description = "Alumnus"

    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = "Full Name"


admin.site.register(CurrentPosition)
admin.site.register(PostdocPosition)
admin.site.register(JobAfterLeaving)




# Change order of models on the admin index, either modify the index.html template
# Or register all models to custom class, then change the app_list and adjust urls.py
# class MyAdminSite(django.contrib.admin.site.AdminSite):
#     def index(self, request, extra_context=None):
#         if extra_context is None:
#             extra_context = {}
#         extra_context["app_list"] = get_app_list_in_custom_order()
#         return super(MyAdminSite, self).index(request, extra_context)
