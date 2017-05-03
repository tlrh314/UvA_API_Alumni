from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import Press, Event, Colloquium, Pizza
from .forms import (PressAdminForm, EventAdminForm, ColloquiumAdminForm,
                    PizzaAdminForm)
from ...settings import ADMIN_MEDIA_JS


class PressAdmin(admin.ModelAdmin):
    form = PressAdminForm
    list_display = ('title', 'date', 'visible')
    ordering = ('-date',)
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'language', 'date',
                     'teaser_text', 'teaser_picture'),
          'classes': ('', )}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible'),
          'classes': ('', )}),
        )

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/news.js',)


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'date', 'visible')
    ordering = ('-date',)
    # get the additional time field near the date field
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'language', 'location',
                     'date', 'date_end', 'time', 'time_end',
                     'teaser_text', 'teaser_picture'),
          'classes': ('', )}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible'),
          'classes': ('', )}),
        )

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/news.js',)


class ColloquiumAdmin(admin.ModelAdmin):
    form = ColloquiumAdminForm
    date_hierarchy = 'date'
    list_display = ('title', 'speaker', 'date', 'visible')
    ordering = ('-date',)
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'speaker', 'affiliation', 'location',
                     'date', 'time',
                     'teaser_text', 'teaser_picture'),
          'classes': ('', )}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible'),
          'classes': ('', )}),
        )

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/news.js',)


class PizzaAdmin(admin.ModelAdmin):
    form = PizzaAdminForm
    date_hierarchy = 'date'
    list_display = ('title', 'speaker', 'shorttalk_speaker', 'date', 'visible')
    ordering = ('-date',)
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'speaker', 'affiliation', 'location',
                     'date', 'time',
                     'teaser_text', 'teaser_picture',
                     'shorttalk_speaker'),
          'classes': ('', )}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible'),
          'classes': ('', )}),
        )

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/news.js',)


# admin.site.register(Press, PressAdmin)
# admin.site.register(Event, EventAdmin)
# admin.site.register(Colloquium, ColloquiumAdmin)
# admin.site.register(Pizza, PizzaAdmin)
