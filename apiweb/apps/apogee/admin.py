from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import Entry
from .forms  import EntryAdminForm

class EntryAdmin(admin.ModelAdmin):

    form = EntryAdminForm

    list_display = ["creator", "date", "title"]
    search_fields = ["title"]
    list_filter = ["creator"]
    ordering = ["-date", "creator",]
    fields = ["creator", "title", "dome", "body", "date", "date_end"]

# admin.site.register(Entry, EntryAdmin)




#
#
#    list_filter = ('last_name', 'first_name')
#    list_display = ('user','email','first_name', 'prefix', 'last_name')
#    search_fields = ('first_name', 'last_name')
#    ordering = ('user__username',)
#    fieldsets = [
#        ('Account information',
#                 {'fields': ['user', 'show_person']}),
#        ('Personal information',
#                 {'fields': ['first_name', 'prefix', 'last_name',
#                             'title', 'initials', 'gender', 'birth_date',
#                             'address', 'zipcode', 'city', 'country',
##                             'home_phone', 'mobile', 'mugshot', 'photo']}),
#        ('Science information',
#                 {'fields': ['position', 'office', 'work_phone',
#                             'ads_name', 'email', 'homepage',
#                             'research', 'contact']}),
#        ('Extra information',
#                 {'fields': ['comments']}),
#    ]
#
