import copy

from django import forms
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from tinymce.widgets import TinyMCE
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

from .models import Category, Post
from ..alumni.models import Alumnus
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG


# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated", "last_updated_by")

    fieldsets = [
        ("Category Names", {
            "fields": ["name",]
        }),
        ("Meta Info", {
            "classes": ["collapse"],
            "fields": ["slug", "date_created", "date_updated", "last_updated_by" ]
        }),
    ]

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["slug"]:
            obj.slug = form.cleaned_data["slug"]
        else:
            obj.slug = slugify(form.cleaned_data["name"])

        # TODO: also change the directory name of the teaser image

        obj.last_updated_by = request.user
        obj.save()


class InterviewAdminForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Post

    # look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    # look["width"] = ""
    # look["height"] = "200"

    # Teaser was a charfield shown as a TinyMCE field. This allowed to
    # copy-paste text/images which preserved formatting and html syntax. This
    # could easily break the front-end as well as the functionality when a rogue
    # user puts crazy stuff in the field. Also, copy-paste as plain text is ignored.
    # teaser = forms.CharField(required=False, widget=TinyMCE(mce_attrs=look))

    author = AutoCompleteSelectField('author', required=True, help_text=None)
    alumnus = AutoCompleteSelectField('alumnus', required=False, show_help_text=False,
        help_text="Select which Alumnus is interviewed.")
        # help_text="Select Alumnus if the Category is an Interview. Leave blank when the Category is News.",)


@admin.register(Post)
class InterviewAdmin(admin.ModelAdmin):
    ordering = ("-date_published", )
    search_fields = ("title", "author", "title", "content")
    list_display = ("author", "title", "get_alumnus", "is_published", "date_published")
    list_filter = ("is_published", )
    exclude = ("category",)
    form = InterviewAdminForm
    # raw_id_fields = ("alumnus",)
    actions = ("publish", "unpublish" )
    readonly_fields = ("date_created", "date_published", "last_updated_by")

    fieldsets = [
        ("Alumni Interview", {
            "fields": ["author", "title", "alumnus", "content", "is_published"]
        }),
        ("Meta Info", {
            "classes": ["collapse"],
            "fields": ["teaser", "slug", "date_created", "date_published", "last_updated_by"]
        }),
    ]

    class Media:
        # The admin actions dropdown is replaced by buttons with a bit of javascript.
        js = ADMIN_MEDIA_JS
        css = {
             "all": ("css/admin_extra.css",)
        }

    def get_form(self, request, obj=None, **kwargs):
        form = super(InterviewAdmin, self).get_form(request, obj, **kwargs)
        alumnus = Alumnus.objects.get(user=request.user)
        form.base_fields["author"].initial = alumnus.id

        # interview = Category.objects.filter(name="Interview")[0]
        # if interview:
        #     form.base_fields["category"].initial = interview

        return form

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["slug"]:
            obj.slug = form.cleaned_data["slug"]
        else:
            obj.slug = slugify(form.cleaned_data["title"])
        if form.cleaned_data["teaser"]:
            obj.teaser = form.cleaned_data["teaser"]
        else:
            obj.teaser = form.cleaned_data["content"][0:500]
        if form.cleaned_data["is_published"] is True:
            obj.publish()


        obj.last_updated_by = request.user
        obj.save()

    def get_alumnus(self, obj):
        """ We could use author instead of get_alumnus in list_display """
        return obj.alumnus.full_name
    get_alumnus.short_description = "Interviewed Alumnus"

    def publish(self, request, queryset):
        for post in queryset:
            post.publish()

            content_type_pk = ContentType.objects.get_for_model(Post).pk
            LogEntry.objects.log_action(
                request.user.pk, content_type_pk, post.pk, str(post), CHANGE,
                change_message="Set status to 'Published'"
            )
        self.message_user(request, "Interview successfully published.")
    publish.short_description = "Publish selected post"

    def unpublish(self, request, queryset):
        for post in queryset:
            post.unpublish()

            content_type_pk = ContentType.objects.get_for_model(Post).pk
            LogEntry.objects.log_action(
                request.user.pk, content_type_pk, post.pk, str(post), CHANGE,
                change_message="Set status to 'Unpublisheded'"
            )
        self.message_user(request, "Interview successfully unpublished.")
    unpublish.short_description = "Unpublish selected post"


