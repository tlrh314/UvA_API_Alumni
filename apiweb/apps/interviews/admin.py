import copy

from django import forms
from django.contrib import admin
from django.template.defaultfilters import slugify

from tinymce.widgets import TinyMCE
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

from .models import Category, Post
from ..alumni.models import Alumnus
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG



@admin.register(Category)
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
    look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    look["width"] = ""
    look["height"] = "200"
    teaser = forms.CharField(required=False, widget=TinyMCE(mce_attrs=look))

    class Meta:
        fields = "__all__"
        model = Post

    # TODO: implement this functionality also in Alumnus admin for User lookup
    alumnus = AutoCompleteSelectField('alumnus', required=False, show_help_text=False,
        help_text="Select Alumnus if the Category is an Interview. Leave blank when the Category is News.",)


    # TODO: author does not work when setting this to request.user in get_form
    # author = AutoCompleteSelectField('author', required=True, help_text=None)


@admin.register(Post)
class InterviewAdmin(admin.ModelAdmin):
    ordering = ("-date_published", )
    search_fields = ("title", "author")
    list_display = ("author", "title", "is_published", "date_published")
    list_filter = ("is_published", )
    form = InterviewAdminForm
    # raw_id_fields = ("alumnus",)
    actions = ("publish", "unpublish" )
    readonly_fields = ("date_created", "date_published", "last_updated_by")

    fieldsets = [
        ("Alumni Interview", {
            "fields": ["author", "title", "category", "alumnus", "content", "is_published"]
        }),
        ("Meta Info", {
            "classes": ["collapse"],
            "fields": ["teaser", "slug", "date_created", "date_published", "last_updated_by"]
        }),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(InterviewAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["author"].initial = request.user

        interview = Category.objects.filter(name="Interview")[0]
        if interview:
            form.base_fields["category"].initial = interview

        return form

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["slug"]:
            obj.slug = form.cleaned_data["slug"]
        else:
            obj.slug = slugify(form.cleaned_data["title"])
        if form.cleaned_data["teaser"]:
            obj.teaser = form.cleaned_data["teaser"]
        else:
            obj.teaser = form.cleaned_data["content"][0:200]

        obj.last_updated_by = request.user
        obj.save()

    # TODO: make publish/unpublish show up in recent actions
    def publish(self, request, queryset):
        for obj in queryset:
            obj.publish()

        self.message_user(request, "Interview successfully published.")
    publish.short_description = "Publish selected post"

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "Interview successfully unpublished.")
    unpublish.short_description = "Unpublish selected post"

