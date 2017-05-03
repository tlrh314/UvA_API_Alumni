from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import WikiPage


class WikiPageAdmin(admin.ModelAdmin):

    list_display = ('name', 'visits', 'creation_author', 'modification_author',
                    'is_category_page', 'is_visible')
    search_fields = ('name',)
    ordering = ('name',)


# admin.site.register(WikiPage, WikiPageAdmin)
