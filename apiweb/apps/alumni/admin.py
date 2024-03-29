import sys

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apiweb import context_processors

from ...settings import ADMIN_MEDIA_JS
from ..research.models import Thesis
from ..survey.admin import JobAfterLeavingAdminInline
from ..survey.forms import SendSurveyForm
from .actions import save_alumni_to_xls
from .filters import EmptyEmailListFilter, EmptyLastCheckedListFilter, SurveyListFilter
from .forms import AlumnusAdminForm, CustomUserCreationForm, PreviousPositionAdminForm
from .models import AcademicTitle, Alumnus, PositionType, PreviousPosition

# Do not show the Site Admin
admin.site.unregister(Group)
admin.site.unregister(Site)


class PreviousPositionInline(admin.StackedInline):
    model = PreviousPosition
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    exclude = ("fte_per_year",)
    extra = 0
    # There are two fk relations with Alumnus, so we must specify which one should be inlined
    fk_name = "alumnus"


@admin.register(PreviousPosition)
class PreviousPositionAdmin(admin.ModelAdmin):
    list_display = (
        "get_alumnus",
        "type",
        "date_start",
        "date_stop",
        "funding",
        "is_last",
    )
    list_filter = ("type", "is_last")
    search_fields = (
        "date_start",
        "date_stop",
        "alumnus__last_name",
        "alumnus__first_name",
    )
    # "alumnus__first_name", "alumnus__last_name",
    ordering = ("alumnus__last_name",)

    form = PreviousPositionAdminForm
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    exclude = ("fte_per_year",)
    extra = 1

    fieldsets = [
        (
            "Previous Position",
            {"fields": ["alumnus", "date_start", "date_stop", "type"]},
        ),
        ("Funding", {"fields": ["nova", "funding", "funding_note", "funding_remark"]}),
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

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def get_queryset(self, request):
        """This function defines how to sort on alumnus column in the list_display"""
        qs = super(PreviousPositionAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count("alumnus"))
        return qs

    def get_alumnus(self, obj):
        return obj.alumnus.full_name

    get_alumnus.short_description = "Alumnus"
    get_alumnus.admin_order_field = "alumnus__last_name"


class ThesisAdminInline(admin.StackedInline):
    extra = 0
    model = Thesis
    filter_horizontal = ("advisor",)
    readonly_fields = ("date_created", "date_updated", "last_updated_by", "slug")
    # There are two fk relations with Alumnus, so we must specify which one should be inlined
    fk_name = "alumnus"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        try:  # Breaks for add alumnus
            current_alumnus = Alumnus.objects.get(pk=request.resolver_match.args[0])
            if db_field.name == "advisor":
                kwargs["queryset"] = Alumnus.objects.exclude(
                    username=current_alumnus.username
                )
            return super(ThesisAdminInline, self).formfield_for_manytomany(
                db_field, request, **kwargs
            )
        except IndexError as e:
            if str(e) == "tuple index out of range":
                pass


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


@admin.register(AcademicTitle)
class AcademicTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Alumnus)
class AlumnusAdmin(UserAdmin):
    form = AlumnusAdminForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    ordering = ("username",)

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "theses__title",
        "theses__date_start",
        "theses__date_stop",
        "theses__date_of_defence",
    )

    list_display = (
        "get_alumnus",
        "email",
        "last_checked",
        "survey_info_updated",
        "survey_email_sent",
        "show_msc_year",
        "show_phd_year",
        "show_postdoc_year",
        "show_staff_year",
        "is_staff",
    )

    list_filter = (
        EmptyEmailListFilter,
        EmptyLastCheckedListFilter,
        "passed_away",
        SurveyListFilter,
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )

    inlines = (ThesisAdminInline, PreviousPositionInline, JobAfterLeavingAdminInline)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    readonly_fields = (
        "get_full_name",
        "date_created",
        "date_updated",
        "survey_info_updated",
        "survey_email_sent",
    )

    actions = (
        "send_password_reset",
        "reset_password_yourself",
        "export_selected_alumni_to_excel",
        "export_all_alumni_to_excel",
        "export_filtered_alumni_to_excel",
        "send_survey_email",
        "send_filtered_alumni_survey_email",
    )

    # To allow execution without checkbox
    extended_actions = (
        "export_all_alumni_to_excel",
        "export_filtered_alumni_to_excel",
        "send_filtered_alumni_survey_email",
    )

    fieldsets = [
        (None, {"fields": ["username", "password", "show_person", "passed_away"]}),
        (
            "Personal information",
            {
                # "classes": ["collapse"],
                "fields": [
                    "academic_title",
                    "initials",
                    "first_name",
                    "prefix",
                    "last_name",
                    "gender",
                    "birth_date",
                    "place_of_birth",
                    "nationality",
                ]
                # "mugshot", "biography"]
            },
        ),
        (
            "Contact information",
            {
                # "classes": ["collapse"],
                "fields": [
                    ("email", "show_email"),
                    ("linkedin", "show_linkedin"),
                    ("facebook", "show_facebook"),
                    ("twitter", "show_twitter"),
                    ("homepage", "show_homepage"),
                    "mobile",
                    "home_phone",
                    "last_checked",
                ]
            },
        ),
        ("Biography", {"fields": ["mugshot", ("biography", "show_biography")]}),
        (
            "Adress information",
            {
                "classes": ["collapse"],
                "fields": [
                    "address",
                    "streetname",
                    "streetnumber",
                    "zipcode",
                    "city",
                    "country",
                ],
            },
        ),
        (
            "Current Position",
            {"classes": ["collapse"], "fields": ["position", "ads_name"]},
        ),
        (
            _("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
        (_("Important dates"), {"fields": ["last_login", "date_joined"]}),
        (
            "Extra information",
            {
                "classes": ["collapse"],
                "fields": [
                    "comments",
                    "date_created",
                    "date_updated",
                    "survey_info_updated",
                    "survey_email_sent",
                ],
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    ]

    class Media:
        js = ADMIN_MEDIA_JS
        css = {"all": ("css/admin_extra.css",)}

    def get_alumnus(self, obj):
        """We could use author instead of get_alumnus in list_display"""
        return obj.full_name

    get_alumnus.short_description = "Alumnus"

    def get_full_name(self, obj):
        return obj.full_name

    get_full_name.short_description = "Full Name"

    def show_staff_year(self, obj):
        if not obj.positions:
            return None

        staff_set = obj.positions.filter(
            type__name__in=[
                "Full Professor",
                "Research Staff",
                "Adjunct Staff",
                "Faculty Staff",
            ]
        )

        if not staff_set:
            return None

        date_stop = staff_set[0].date_stop
        for pos in staff_set:
            if not pos.date_stop:
                continue
            if pos.date_stop > date_stop:
                date_stop = pos.date_stop

        if not date_stop:
            return "Current"
        else:
            return date_stop.strftime("%Y")

    show_staff_year.short_description = "STAFF"

    def show_postdoc_year(self, obj):
        postdoc = PositionType.objects.filter(name="Postdoc")
        if len(postdoc) == 1:
            postdoc = postdoc[0]

        # CAUTION, position is the current position while the related name of PreviousPosition is positions !!
        if obj.position == postdoc:
            return "Current"

        postdoc_set = obj.positions.filter(type=postdoc)
        if len(postdoc_set) == 0:
            return "-"

        # Could have multiple date_stop
        postdoc = postdoc_set[0]
        for pd in postdoc_set:
            if pd.date_stop > postdoc.date_stop:
                postdoc = pd
        if postdoc.date_stop:
            return postdoc.date_stop.strftime("%Y")

    show_postdoc_year.short_description = "PD"

    def show_phd_year(self, obj):
        theses = obj.theses.filter(type="phd")
        if len(theses) != 0:
            if theses[0].date_of_defence:
                return theses[0].date_of_defence.strftime("%Y")
            elif theses[0].date_stop:
                return theses[0].date_stop.strftime("%Y")
        return None

    show_phd_year.short_description = "PhD"

    def show_msc_year(self, obj):
        theses = obj.theses.filter(type="msc")
        if len(theses) != 0:
            if theses[0].date_of_defence:
                return theses[0].date_of_defence.strftime("%Y")
            elif theses[0].date_stop:
                return theses[0].date_stop.strftime("%Y")
        return None

    show_msc_year.short_description = "MSc"

    def send_password_reset(self, request, queryset):
        for alumnus in queryset:
            try:
                validate_email(alumnus.email)
                form = PasswordResetForm(data={"email": alumnus.email})
                form.is_valid()

                # Get ContactInfo from context_processors such that the forced
                # reset email footer has the email address and phone number of API
                contactdict = context_processors.contactinfo(request)

                form.save(
                    email_template_name="registration/password_forced_reset_email.html",
                    extra_email_context={
                        "full_name": alumnus.full_name,
                        "secretary_email_address": contactdict[
                            "contactinfo"
                        ].secretary_email_address,
                        "api_phonenumber_formatted": contactdict[
                            "api_phonenumber_formatted"
                        ],
                    },
                )
                self.message_user(request, "Succesfully sent password reset email.")
            except ValidationError:
                self.message_user(
                    request,
                    "Alumnus does not have a valid email address",
                    level="error",
                )

    send_password_reset.short_description = "Send selected Alumni Password Reset"

    def send_survey_email(self, request, queryset):
        exclude_alumni = []
        reason = []

        # Get ContactInfo from context_processors such that the forced
        # reset email footer has the email address and phone number of API
        contactdict = context_processors.contactinfo(request)

        for alumnus in queryset:
            if alumnus.passed_away:
                exclude_alumni.append(alumnus)
                reason.append("Passed Away")
                continue
            if not alumnus.email:
                exclude_alumni.append(alumnus)
                reason.append("Invalid Email")
                continue

            print("Sending email to", alumnus)
            try:
                validate_email(alumnus.email)
                form = SendSurveyForm(data={"email": alumnus.email, "alumnus": alumnus})
                form.is_valid()
                form.save(
                    alumnus=alumnus,
                    extra_email_context={
                        "full_name_no_title": alumnus.full_name_no_title,
                        "secretary_email_address": contactdict[
                            "contactinfo"
                        ].secretary_email_address,
                        "api_phonenumber_formatted": contactdict[
                            "api_phonenumber_formatted"
                        ],
                    },
                )
                alumnus.survey_email_sent = timezone.now()
                alumnus.save()
            except ValidationError:
                exclude_alumni.append(alumnus)
                reason.append("ValidationError")

        if "runserver" in sys.argv:
            self.message_user(
                request,
                "The Survey Email was Successfully Sent to the terminal to "
                + "{0} alumni (because this is development)!".format(
                    str(queryset.count() - len(exclude_alumni))
                ),
            )
        else:
            # Probably success for most, but report if email broke.
            self.message_user(
                request,
                "The Survey Email was Successfully sent to {0} alumni!".format(
                    str(queryset.count() - len(exclude_alumni))
                ),
            )

        for alum, why in zip(exclude_alumni, reason):
            msg = "The following Alumnus was excluded: {0} ({1}).".format(alum, why)
            self.message_user(request, msg, level="error")

    send_survey_email.short_description = "Send selected Alumni Survey Email"

    def send_filtered_alumni_survey_email(self, request, queryset):
        queryset = self.get_filtered_queryset(request)
        self.send_survey_email(request, queryset)

    send_filtered_alumni_survey_email.short_description = (
        "Send filtered list of Alumni Survey Email"
    )

    def reset_password_yourself(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, "Please select only one Alumnus!", level="error")
        else:
            userpk = queryset[0].pk
            return HttpResponseRedirect(
                "/admin/alumni/alumni/{0}/password/".format(userpk)
            )

    reset_password_yourself.short_description = "Reset password of Alumnus yourself"

    def export_selected_alumni_to_excel(self, request, queryset):
        return save_alumni_to_xls(request, queryset)
        # self.message_user(request, "This function is not yet implemented.", level="error")

    export_selected_alumni_to_excel.short_description = (
        "Export selected Alumni to Excel"
    )

    def export_all_alumni_to_excel(self, request, queryset):
        return save_alumni_to_xls(request, None)
        # self.message_user(request, "This function is not yet implemented.", level="error")

    export_all_alumni_to_excel.short_description = "Export all Alumni to Excel"

    # In this function, I override the queryset. If the user wants to select
    # (with checkbox) they can use 'export selected..'
    # This override will ignore the queryset of checkboxes but will use the
    # get_filtered_queryset result value, based on the active filters
    def export_filtered_alumni_to_excel(self, request, queryset):
        queryset = self.get_filtered_queryset(request)
        return save_alumni_to_xls(request, queryset)

    export_filtered_alumni_to_excel.short_description = (
        "Export filtered list of Alumni to Excel"
    )


@admin.register(PositionType)
class PositionTypeAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated")
