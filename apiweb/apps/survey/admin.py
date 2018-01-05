from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.contrib import admin

from .models import Sector
from .models import JobAfterLeaving
from .actions import save_all_jobs_to_xls
from ...settings import ADMIN_MEDIA_JS

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

# Copied from https://gist.github.com/rafen/eff7adae38903eee76600cff40b8b659, also present in theses admin and jobs admin
class ExtendedActionsMixin(object):
    # actions that can be executed with no items selected on the admin change list.
    # The filtered queryset displayed to the user will be used instead
    extended_actions = []

    def changelist_view(self, request, extra_context=None):
        # if a extended action is called and there's no checkbox selected, select one with
        # invalid id, to get an empty queryset
        if 'action' in request.POST and request.POST['action'] in self.extended_actions:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({admin.ACTION_CHECKBOX_NAME: 0})
                request._set_post(post)
        return super(ExtendedActionsMixin, self).changelist_view(request, extra_context)

    def get_changelist_instance(self, request):
        """
        Returns a simple ChangeList view instance of the current ModelView.
        (It's a simple instance since we don't populate the actions and list filter
        as expected since those are not used by this class)
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        list_select_related = self.get_list_select_related(request)

        ChangeList = self.get_changelist(request)

        return ChangeList(
            request, self.model, list_display,
            list_display_links, list_filter, self.date_hierarchy,
            search_fields, list_select_related, self.list_per_page,
            self.list_max_show_all, self.list_editable, self,
        )

    def get_filtered_queryset(self, request):
        """
        Returns a queryset filtered by the URLs parameters
        """
        cl = self.get_changelist_instance(request)
        return cl.get_queryset(request)

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated", "last_updated_by")


class JobAfterLeavingAdminInline(admin.StackedInline):
    model = JobAfterLeaving
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    extra = 0
    # There are two fk relations with Alumnus, so we must specify which one should be inlined
    fk_name = "alumnus"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

class JobAfterLeavingAdminForm(forms.ModelForm):
    alumnus = AutoCompleteSelectField('alumnus', required=True, help_text=None)
    # TODO: how to django_ajax without a model, but on the dict django_countries.data.COUNTRIES ?
    # location_job = AutoCompleteSelectField('location_job', required=True, help_text=None)

@admin.register(JobAfterLeaving)
class JobAfterLeavingAdmin(ExtendedActionsMixin, admin.ModelAdmin):
    list_display = ("alumnus", "which_position", "show_job", "sector", "company_name", "position_name", 
        "is_inside_academia", "is_inside_astronomy", "location_job", "start_date", "stop_date")
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    list_filter = ("which_position", "is_inside_academia", "is_inside_astronomy", "sector", )

    actions = ("export_selected_jobs_to_excel", "export_all_jobs_to_excel", "export_filtered_jobs_to_excel",)
    extended_actions = ('export_all_jobs_to_excel', 'export_filtered_jobs_to_excel',)

    form = JobAfterLeavingAdminForm

    fieldsets = [
        ( "Job information", {
            "fields":
                [ "alumnus", "which_position", "sector", "company_name", "position_name", "location_job",
                  "is_inside_academia", "is_inside_astronomy", "start_date", "stop_date" ]
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

    #Actions
    def export_selected_jobs_to_excel(self, request, queryset):
        return save_all_jobs_to_xls(request, queryset)
    export_selected_jobs_to_excel.short_description = "Export selected Jobs to Excel"

    def export_all_jobs_to_excel(self, request, queryset):
        return save_all_jobs_to_xls(request, None)
    export_all_jobs_to_excel.short_description = "Export all Jobs to Excel"

    def export_filtered_jobs_to_excel(self, request, queryset):
        queryset = self.get_filtered_queryset(request)
        return save_all_jobs_to_xls(request, queryset)
    export_filtered_jobs_to_excel.short_description = "Export filtered list of Jobs to Excel"

