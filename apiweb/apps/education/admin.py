from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import BachelorProject, MasterProject, CourseTopic
from ...settings import ADMIN_MEDIA_JS


class BachelorProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact',)
    #exclude = ('slug',)
    ordering = ('-academic_year',)
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'year', 'academic_year', 'contact'),
          'classes': ('',)}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible',),
          'classes': ('',)}),
        )


class MasterProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact',)
    ordering = ('-academic_year',)
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'year', 'academic_year', 'contact'),
          'classes': ('',)}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible',),
          'classes': ('',)}),
        )

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/news.js',)


class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'semester')
    ordering = ('semester', 'name')


admin.site.register(BachelorProject, BachelorProjectAdmin)
admin.site.register(MasterProject, MasterProjectAdmin)
admin.site.register(CourseTopic, CourseTopicAdmin)
