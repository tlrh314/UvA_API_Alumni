from __future__ import unicode_literals, absolute_import, division
import copy

from django import forms
from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.http.response import HttpResponseRedirect
from django.contrib.sites.models import Site
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE
# from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from apiweb import context_processors
from .models import PositionType, PreviousPosition
from .models import Alumnus, Degree, JobAfterLeaving
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG
from .actions import save_all_alumni_to_xls, save_all_theses_to_xls


# Do not show the Site Admin
# admin.site.unregister(Site)

# Do not allow the Admin to change the User first_name, last_name or email.
# The Alumnus has these fields, and when these fields are updated a signal is
# sent from the Alumnus to the User to update the email, first_name and last_name
# If the Admin could change these fields in the User there would be a mismatch.
UserAdmin.readonly_fields = ("email", "first_name", "last_name")
UserAdmin.fieldsets = (
    (None, {"fields": ("username", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "email"),
        "description": "Please change the personal info in the Alumnus Admin."}),
    (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
                                   "groups", "user_permissions")}),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class JobAfterLeavingAdminInline(admin.StackedInline):
    model = JobAfterLeaving
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(JobAfterLeaving)
class JobAfterLeavingAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated", "last_updated_by")

    fieldsets = [
        ( "Job information", {
            "fields":
                [ "position_name", "current_job", "company_name", "start_date",
                "stop_date", "inside_academia", "location_job" ]
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


class PreviousPositionInline(admin.StackedInline):
    model = PreviousPosition
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    exclude = ("fte_per_year",)
    extra = 0


class PreviousPositionAdminForm(forms.ModelForm):
    nova = forms.MultipleChoiceField(widget=forms.RadioSelect(), choices=PreviousPosition.NOVA_NETWORK)
    # Remove following line for dropdown.
    funding = forms.MultipleChoiceField(widget=forms.RadioSelect(), choices=PreviousPosition.FUNDING)


@admin.register(PreviousPosition)
class PreviousPositionAdmin(admin.ModelAdmin):
    list_display = ("get_alumnus", "type", "date_start", "date_stop", "funding", "is_last")
    list_filter = ("type", "is_last")
    search_fields = ("date_start", "date_stop", "alumnus__last_name", "alumnus__first_name")
    # "alumnus__first_name", "alumnus__last_name",
    ordering = ("alumnus__last_name", )

    form = PreviousPositionAdminForm
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    exclude = ("fte_per_year",)
    extra = 1

    fieldsets = [
        ( "Previous Position", {
            "fields":
                [ "alumnus", "date_start", "date_stop", "type"]
            }
        ), ( "Funding", {
            "fields":
                [ "nova", "funding", "funding_note", "funding_remark" ]
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

    def get_queryset(self, request):
        """ This function defines how to sort on alumnus column in the list_display """
        qs = super(PreviousPositionAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count("alumnus"))
        return qs

    def get_alumnus(self, obj):
        return obj.alumnus.full_name
    get_alumnus.short_description = "Alumnus"
    get_alumnus.admin_order_field = "alumnus__last_name"


class DegreeAdminInline(admin.StackedInline):
    extra = 0
    model = Degree
    filter_horizontal = ("thesis_advisor", )
    readonly_fields = ("date_created", "date_updated", "last_updated_by")


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
            return queryset.filter(thesis_title__isnull=False).exclude(thesis_title="")

        if self.value() == "yes":
            return queryset.filter(Q(thesis_title__isnull=True) | Q(thesis_title__exact=""))


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ("get_author", "thesis_title", "show_year", "type")
    list_filter = ("type", DegreeListFilter)
    search_fields = ("thesis_title", "alumnus__last_name", "alumnus__first_name",
        "date_start", "date_stop", "date_of_defence")
    ordering = ("alumnus__user__username", )
    filter_horizontal = ("thesis_advisor", )
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    actions = ("export_selected_degrees_to_excel", "export_all_degrees_to_excel", )

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
                "fields": ["comments",  "date_created", "date_updated", "last_updated_by"]
            }
        ),
    ]

    class Media:
        js = ADMIN_MEDIA_JS
        css = {
             "all": ("css/admin_extra.css",)
        }

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def changelist_view(self, request, extra_context=None):
        """ Hack the default changelist_view to allow action "export_all_degrees_to_excel"
            to run without selecting any objects """
        if "action" in request.POST and request.POST["action"] == "export_all_degrees_to_excel":
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Degree.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(DegreeAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        """ This function defines how to sort on alumnus column in the list_display
            http://stackoverflow.com/a/29083623 """
        qs = super(DegreeAdmin, self).get_queryset(request)
        qs = qs.annotate()
        # TODO: this does not take into account the type of the Degree. Also, when
        # filtering on type = "PhD" ordering of the Degrees could be done on the MSc degree
        qs = qs.annotate(sort_author = models.Count("alumnus__last_name", distinct=True)).annotate(sort_year =
                models.Count("alumnus__degrees__date_of_defence", distinct=True))
        return qs

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
    export_selected_degrees_to_excel.short_description = "Export selected Theses to Excel"

    def export_all_degrees_to_excel(self, request, queryset):
        return save_all_theses_to_xls(request, None)
    export_all_degrees_to_excel.short_description = "Export all Theses to Excel"


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
    biography = forms.CharField(required=False, widget=TinyMCE(mce_attrs=look))

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
            return queryset.filter(email__isnull=False).exclude(email="")

        if self.value() == "yes":
            return queryset.filter(Q(email__isnull=True) | Q(email__exact=""))


@admin.register(Alumnus)
class AlumnusAdmin(admin.ModelAdmin):
    ordering = ("user__username", )
    search_fields = ("first_name", "last_name", "degrees__thesis_title",
        "degrees__date_start", "degrees__date_stop", "degrees__date_of_defence")
    list_display = ("get_alumnus", "email", "show_msc_year", "show_phd_year", "show_postdoc_year", "show_staff_year")
    list_filter = ("show_person", AlumnusListFilter)  # position and positions (== related name of PreviousPosition)
    inlines = (DegreeAdminInline, PreviousPositionInline, JobAfterLeavingAdminInline)
    form = AlumnusAdminForm
    filter_horizontal = ("research", "contact", )
    readonly_fields = ("get_full_name", "date_created", "date_updated", "last_updated_by")
    actions = ("sent_password_reset", "reset_password_yourself",
               "export_selected_alumni_to_excel", "export_all_alumni_to_excel")
    # exclude = ("jobs", )

    fieldsets = [
        ("Account information",
                {
                    "fields": ["user", "get_full_name", "show_person"]
                }),

        ("Personal information", {
                "classes": ["collapse"],
                 "fields": ["first_name", "prefix", "last_name",
                             "title", "initials", "gender", "birth_date",
                             "place_of_birth", "nationality",]
                             # "mugshot", "photo", "biography"]
                }),

        ("Contact information", {
                # "classes": ["collapse"],
                "fields":["email", "linkedin", "facebook", "twitter", "homepage",
                          "mobile", "home_phone", "last_checked"]
                }),

        ("Biography", {
                 "fields": [ "mugshot", "photo", "biography"]
                }),

        ("Adress information", {
                "classes": ["collapse"],
                "fields": ["address", "streetname", "streetnumber", "zipcode",
                           "city", "country"]
                }),

        ("Current Position", {
                "classes": ["collapse"],
                 "fields": ["position", "office", "work_phone",
                             "ads_name", "research", "contact"]
                }),

        ("Extra information", {
                "classes": ["collapse"],
                "fields": ["comments",  "date_created", "date_updated", "last_updated_by"]
                }),
    ]

    class Media:
        js = ADMIN_MEDIA_JS
        css = {
             "all": ("css/admin_extra.css",)
        }

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


    def changelist_view(self, request, extra_context=None):
        """ Hack the default changelist_view to allow action "export_all_alumni_to_excel"
            to run without selecting any objects """
        if "action" in request.POST and request.POST["action"] == "export_all_alumni_to_excel":
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Alumnus.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(AlumnusAdmin, self).changelist_view(request, extra_context)

    def get_alumnus(self, obj):
        """ We could use author instead of get_alumnus in list_display """
        return obj.full_name
    get_alumnus.short_description = "Alumnus"

    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = "Full Name"

    def show_staff_year(self, obj):
        if not obj.positions:
            return None

        staff_set = obj.positions.filter(type__name__in=["Full Professor", "Research Staff",
            "Adjunct Staff", "Faculty Staff"])

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
        postdoc = PositionType.objects.filter(name="Postdoc")[0]

        # CAUTION, position is the current position while the related name of PreviousPosition is positions !!
        if obj.position == postdoc:
            return "Current"

        postdoc_set = obj.positions.filter(type=postdoc)
        if len(postdoc_set) is 0:
            return None

        # Could have multiple date_stop
        postdoc = postdoc_set[0]
        for pd in postdoc_set:
            if pd.date_stop > postdoc.date_stop:
                postdoc = pd
        if postdoc.date_stop:
            return postdoc.date_stop.strftime("%Y")
    show_postdoc_year.short_description = "PD"

    def show_phd_year(self, obj):
        degrees = obj.degrees.filter(type="phd")
        if len(degrees) is not 0:
            if degrees[0].date_of_defence:
                return degrees[0].date_of_defence.strftime("%Y")
            elif degrees[0].date_stop:
                return degrees[0].date_stop.strftime("%Y")
        return None
    show_phd_year.short_description = "PhD"

    def show_msc_year(self, obj):
        degrees = obj.degrees.filter(type="msc")
        if len(degrees) is not 0:
            if degrees[0].date_of_defence:
                return degrees[0].date_of_defence.strftime("%Y")
            elif degrees[0].date_stop:
                return degrees[0].date_stop.strftime("%Y")
        return None
    show_msc_year.short_description = "MSc"

    def sent_password_reset(self, request, queryset):
        for alumnus in queryset:
            if alumnus.user.email != alumnus.email:
                alumnus.user.email = alumnus.email
                alumnus.save()
            try:
                validate_email( alumnus.email )
                form = PasswordResetForm(data={"email": alumnus.email})
                form.is_valid()

                # Get ContactInfo from context_processors such that the forced
                # reset email footer has the email address and phone number of API
                contactdict = context_processors.contactinfo(request)

                form.save(email_template_name="registration/password_forced_reset_email.html",
                          extra_email_context = {
                                "full_name": alumnus.full_name,
                                "secretary_email_address": contactdict["contactinfo"].secretary_email_address,
                                "api_phonenumber_formatted": contactdict["api_phonenumber_formatted"]
                              })
                self.message_user(request, "Succesfully sent password reset email.")
            except ValidationError:
                self.message_user(request, "Alumnus does not have a valid email address", level="error")
    sent_password_reset.short_description = "Sent selected Alumni Password Reset"

    def reset_password_yourself(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, "Please select only one Alumnus!", level="error")
        else:
            userpk = queryset[0].user_id
            return HttpResponseRedirect("/admin/auth/user/{0}/password/".format(userpk))
    reset_password_yourself.short_description = "Reset password of Alumnus yourself"

    def export_selected_alumni_to_excel(self, request, queryset):
        return save_all_alumni_to_xls(request, queryset)
        self.message_user(request, "This function is not yet implemented.", level="error")
    export_selected_alumni_to_excel.short_description = "Export selected Alumni to Excel"

    def export_all_alumni_to_excel(self, request, queryset):
        return save_all_alumni_to_xls(request, None)
        # self.message_user(request, "This function is not yet implemented.", level="error")
    export_all_alumni_to_excel.short_description = "Export all Alumni to Excel"


@admin.register(PositionType)
class PositionTypeAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated")



# Change order of models on the admin index, either modify the index.html template
# Or register all models to custom class, then change the app_list and adjust urls.py
# class MyAdminSite(django.contrib.admin.site.AdminSite):
#     def index(self, request, extra_context=None):
#         if extra_context is None:
#             extra_context = {}
#         extra_context["app_list"] = get_app_list_in_custom_order()
#         return super(MyAdminSite, self).index(request, extra_context)
