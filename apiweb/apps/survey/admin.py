from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.contrib import admin

from .models import Sector
from .models import SurveyText
from .models import JobAfterLeaving
from ...settings import ADMIN_MEDIA_JS

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated", "last_updated_by")


@admin.register(SurveyText)
class SurveyTextAdmin(admin.ModelAdmin):
    list_display = ("rename_text",)

    class Media:
        # The admin actions dropdown is replaced by buttons with a bit of javascript.
        js = ADMIN_MEDIA_JS
        css = {
             "all": ("css/admin_extra.css",)
        }

    def rename_text(self, obj):
       return "Click here to change the Survey Text"
    rename_text.short_description = "Survey Text"


class JobAfterLeavingAdminInline(admin.StackedInline):
    model = JobAfterLeaving
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


class JobAfterLeavingAdminForm(forms.ModelForm):
    alumnus = AutoCompleteSelectField('alumnus', required=True, help_text=None)
    # TODO: how to django_ajax without a model, but on the dict django_countries.data.COUNTRIES ?
    # location_job = AutoCompleteSelectField('location_job', required=True, help_text=None)



@admin.register(JobAfterLeaving)
class JobAfterLeavingAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated", "last_updated_by")

    form = JobAfterLeavingAdminForm

    fieldsets = [
        ( "Job information", {
            "fields":
                [ "alumnus", "sector", "company_name", "position_name", "location_job",
                  "is_inside_academia", "is_current_job",  "start_date", "stop_date" ]
            }
        ), ( "Extra information", {
                "classes": ["collapse"],
                "fields": ["comments",  "date_created", "date_updated", "last_updated_by"]
            }
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    class Media:
        # The admin actions dropdown is replaced by buttons with a bit of javascript.
        js = ADMIN_MEDIA_JS
        css = {
             "all": ("css/admin_extra.css",)
        }
