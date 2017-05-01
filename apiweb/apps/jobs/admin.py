from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import Job
from .forms import JobAdminForm
from ...settings import ADMIN_MEDIA_JS


class JobAdmin(admin.ModelAdmin):
    form = JobAdminForm
    date_hierarchy = 'deadline'
    list_display = ('title', 'deadline', 'visible')
    ordering = ('-deadline',)
    fieldsets = (
        (None,
         {'fields': ('title', 'text', 'deadline', 'contact', 'website',
                     'teaser'),
          'classes': ('', )}),
        ('Visibility on site',
         {'fields': ('date_on', 'date_off', 'visible'),
          'classes': ('', )}),
        )

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/jobs.js',)


admin.site.register(Job, JobAdmin)
