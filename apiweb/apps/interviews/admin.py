import copy

from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE


from .models import Post
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG


class InterviewAdminForm(forms.ModelForm):
    look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    look["width"] = ""
    look["height"] = "200"
    teaser = forms.CharField(required=False, widget=TinyMCE(mce_attrs=look))

    class Meta:
        fields = "__all__"
        model = Post


@admin.register(Post)
class InterviewAdmin(admin.ModelAdmin):
    ordering = ("-date_published", )
    search_fields = ("title", "author")
    list_display = ("author", "title", "is_published", "date_published")
    list_filter = ("is_published", )
    form = InterviewAdminForm
    actions = ("publish", "unpublish" )
    readonly_fields = ("date_created", "date_published")

    fieldsets = [
        ("Alumni Interview", {
            "fields": ["author", "title", "content", "is_published"]
        }),
        ("Meta Info", {
            "classes": ["collapse"],
            "fields": ["teaser", "slug", "date_created", "date_published"]
        }),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(InterviewAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["author"].initial = request.user
        return form

    def publish(self, request, queryset):
        for obj in queryset:
            obj.publish()

    publish.short_description = "Publish selected post"

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
    unpublish.short_description = "Unpublish selected post"

