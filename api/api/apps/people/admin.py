from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):

    list_filter = ('show_person', 'position')
    list_display = ('user','email','show_person', 'first_name', 'prefix', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('user__username',)
    fieldsets = [
        ('Account information',
                 {'fields': ['user', 'show_person']}),
        ('Personal information',
                 {'fields': ['first_name', 'prefix', 'last_name',
                             'title', 'initials', 'gender', 'birth_date',
                             'address', 'zipcode', 'city', 'country',
                             'home_phone', 'mobile', 'mugshot', 'photo']}),
        ('Science information',
                 {'fields': ['position', 'office', 'work_phone',
                             'ads_name', 'email', 'homepage',
                             'research', 'contact']}),
        ('Extra information',
                 {'fields': ['comments']}),
    ]


admin.site.register(Person, PersonAdmin)

