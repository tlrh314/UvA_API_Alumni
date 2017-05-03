from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import Staffmeeting


class StaffmeetingAdmin(admin.ModelAdmin):

    list_display = ('date', 'agenda')
    ordering = ('-date',)
    fieldsets = [
        ('Staff meeting information',
         {'fields': ['date']}),
        ('Documents for staff only',
         {'fields': ['agenda', 'report', 'appendix_1',
                     'appendix_2', 'appendix_3']}),
        ('Documents for all employees',
         {'fields': ['decisions', 'appendix_A', 'appendix_B']}),
    ]


# admin.site.register(Staffmeeting, StaffmeetingAdmin)
