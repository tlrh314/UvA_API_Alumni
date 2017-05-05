from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import ResearchTopic, Thesis
from ...settings import ADMIN_MEDIA_JS


class ResearchTopicAdmin(admin.ModelAdmin):

    list_filter = ('topic',)
    list_display = ('topic',)
    search_fields = ('topic',)
    fields = ('topic', 'category', 'picture', 'description')

    class Media:
        js = ADMIN_MEDIA_JS


class ThesisAdmin(admin.ModelAdmin):

    list_filter = ('author',)
    list_display = ('author', 'gender', 'date', 'title')
    search_fields = ('author', 'title')
    ordering = ('-date',)
    fields = ('author', 'gender', 'title', 'date', 'type', 'url')


admin.site.register(ResearchTopic, ResearchTopicAdmin)
admin.site.register(Thesis, ThesisAdmin)
