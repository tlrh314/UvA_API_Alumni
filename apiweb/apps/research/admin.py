from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ...settings import ADMIN_MEDIA_JS
from .actions import save_all_theses_to_xls
from .models import Thesis


# Copied from https://gist.github.com/rafen/eff7adae38903eee76600cff40b8b659,
# also present in theses admin and jobs admin
class ExtendedActionsMixin(object):
    # actions that can be executed with no items selected on the admin change list.
    # The filtered queryset displayed to the user will be used instead
    extended_actions = []

    def changelist_view(self, request, extra_context=None):
        # if a extended action is called and there's no checkbox selected, select one with
        # invalid id, to get an empty queryset
        if "action" in request.POST and request.POST["action"] in self.extended_actions:
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
            request,
            self.model,
            list_display,
            list_display_links,
            list_filter,
            self.date_hierarchy,
            search_fields,
            list_select_related,
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            self.sortable_by,
        )

    def get_filtered_queryset(self, request):
        """
        Returns a queryset filtered by the URLs parameters
        """
        cl = self.get_changelist_instance(request)
        return cl.get_queryset(request)


class ThesisListFilter(admin.SimpleListFilter):
    title = _("empty thesis title")
    parameter_name = "have_title"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "no":
            return queryset.filter(title__isnull=False).exclude(title="")

        if self.value() == "yes":
            return queryset.filter(Q(title__isnull=True) | Q(title__exact=""))


@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ("get_author", "title", "show_year", "type")
    list_filter = ("type", ThesisListFilter)
    search_fields = (
        "title",
        "alumnus__last_name",
        "alumnus__first_name",
        "date_start",
        "date_stop",
        "date_of_defence",
    )
    ordering = ("alumnus__username",)
    filter_horizontal = ("advisor",)
    readonly_fields = (
        "date_created",
        "date_updated",
        "last_updated_by",
        "slug",
    )
    actions = (
        "export_selected_degrees_to_excel",
        "export_all_degrees_to_excel",
        "export_filtered_degrees_to_excel",
    )
    extended_actions = (
        "export_all_degrees_to_excel",
        "export_filtered_degrees_to_excel",
    )

    max_num = 2

    fieldsets = [
        (
            "Thesis Information",
            {"fields": ["alumnus", "type", "date_start", "date_stop"]},
        ),
        (
            "Thesis Information",
            {
                "fields": [
                    "title",
                    "date_of_defence",
                    "url",
                    "dissertation_nr",
                    "slug",
                    "in_library",
                ]
            },
        ),
        ("Thesis Advisor ", {"fields": ["advisor"]}),
        ("Full Text and Cover Photo", {"fields": ["pdf", "photo"]}),
        (
            "Extra information",
            {
                "classes": ["collapse"],
                "fields": [
                    "comments",
                    "date_created",
                    "date_updated",
                    "last_updated_by",
                ],
            },
        ),
    ]

    class Media:
        js = ADMIN_MEDIA_JS
        css = {"all": ("css/admin_extra.css",)}

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    # def changelist_view(self, request, extra_context=None):
    #     """ Hack the default changelist_view to allow action "export_all_degrees_to_excel"
    #         to run without selecting any objects """
    #     if "action" in request.POST and request.POST["action"] == "export_all_degrees_to_excel":
    #         if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
    #             post = request.POST.copy()
    #             for u in Thesis.objects.all():
    #                 post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
    #             request._set_post(post)
    #     return super(ThesisAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        """This function defines how to sort on alumnus column in the list_display
        http://stackoverflow.com/a/29083623"""
        qs = super(ThesisAdmin, self).get_queryset(request)
        qs = qs.annotate()
        # TODO: this does not take into account the type of the Thesis. Also, when
        # filtering on type = "PhD" ordering of the Theses could be done on the MSc Thesis
        qs = qs.annotate(
            sort_author=models.Count("alumnus__last_name", distinct=True)
        ).annotate(
            sort_year=models.Count("alumnus__theses__date_of_defence", distinct=True)
        )
        return qs

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     try:  # Breaks for add thesis
    #         current_thesis = Thesis.objects.get(pk=request.resolver_match.args[0])
    #         if db_field.name == "advisor":
    #             kwargs["queryset"] = Alumnus.objects.exclude(username=current_thesis.alumnus.username)
    #         return super(ThesisAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    #     except IndexError as e:
    #         if str(e) == "tuple index out of range":
    #             pass

    def get_author(self, obj):
        """ We could use author instead of get_alumnus in list_display """
        return obj.alumnus.full_name

    get_author.short_description = "Author"
    get_author.admin_order_field = "sort_author"

    def show_year(self, obj):
        if obj.date_of_defence:
            return obj.date_of_defence.strftime("%Y")
        elif obj.date_stop:
            return obj.date_stop.strftime("%Y")
        return None

    show_year.short_description = "Year"
    show_year.admin_order_field = "sort_year"

    def export_selected_degrees_to_excel(self, request, queryset):
        return save_all_theses_to_xls(request, queryset)

    export_selected_degrees_to_excel.short_description = (
        "Export selected Theses to Excel"
    )

    def export_all_degrees_to_excel(self, request, queryset):
        return save_all_theses_to_xls(request, None)

    export_all_degrees_to_excel.short_description = "Export all Theses to Excel"

    def export_filtered_degrees_to_excel(self, request, queryset):
        queryset = self.get_filtered_queryset(request)
        return save_all_theses_to_xls(request, queryset)

    export_filtered_degrees_to_excel.short_description = (
        "Export filtered list of Theses to Excel"
    )
