from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import Starnight, Activity, StarnightApplicant

class StarnightAdmin(admin.ModelAdmin):
    list_filter = ('date', 'is_registrable')
    list_display = ('date', 'is_registrable', 'max_people')
    ordering = ('-date', )
    fields = ('date', 'is_registrable', 'max_people')

admin.site.register(Starnight, StarnightAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('nr', 'is_in_block1', 'is_in_block2', 'is_in_block3', 'name')
    list_display = ('nr', 'is_in_block1', 'is_in_block2', 'is_in_block3',
                    'name', 'max_people')
    ordering = ('nr', )
    fields = ('nr', 'is_in_block1', 'is_in_block2', 'is_in_block3', 'name',
              'max_people')

admin.site.register(Activity, ActivityAdmin)


class StarnightApplicantAdmin(admin.ModelAdmin):

    list_filter = ('date', 'city', 'newsletter')
    list_display = ('email',)
    list_display = ('date', 'name', 'number', 'slot1', 'slot2', 'slot3')
    search_fields = ('date', 'name', 'number')
    ordering = ('-date', 'name',)
    fields = ('date', 'name', 'address', 'zipcode', 'city', 'email',
              'newsletter', 'number', 'slot1', 'slot2', 'slot3')

admin.site.register(StarnightApplicant, StarnightApplicantAdmin)
