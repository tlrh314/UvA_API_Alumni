from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import Alumnus, Job, MastersDegree, PhdDegree, PostdocPosition, MasterThesis, PhdThesis
from ...settings import ADMIN_MEDIA_JS



class JobAdminInline(NestedStackedInline):
    model = Job
    extra = 1
    fieldsets = [
    ('Job information',
        {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
        )
    ]

class MasterThesisInline(NestedStackedInline):
    model = MasterThesis
    extra = 1

class PhdThesisInline(NestedStackedInline):
    model = PhdThesis
    extra = 1

class MastersDegreeAdminInline(NestedStackedInline):
    model = MastersDegree
    max_num = 1
    inlines = (MasterThesisInline,)
    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]


class PhdDegreeAdminInline(NestedStackedInline):
    model = PhdDegree
    max_num = 1
    inlines = (PhdThesisInline,)
    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]


class PostdocPositionAdminInline(NestedStackedInline):
    model = PostdocPosition
    max_num = 1

    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]


class AlumnusAdmin(NestedModelAdmin):
    list_filter = ('show_person', 'position')
    list_display = ('user','email','show_person', 'first_name', 'prefix', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('user__username',)
    inlines = (JobAdminInline, MastersDegreeAdminInline,
        PhdDegreeAdminInline, PostdocPositionAdminInline)
    # exclude = ('jobs',)


    fieldsets = [
        ('Account information',
                {
                'fields': ['user', 'show_person']
                }),

        ('Personal information',{
                 'fields': ['first_name', 'prefix', 'last_name',
                             'title', 'initials', 'gender', 'birth_date',
                             'place_of_birth', 'nationality', 'mugshot',
                             'photo', 'biography']
                }),

        ('Contact information',{
                'fields':['linkedin', 'facebook', 'email', 'home_phone',
                          'homepage', 'mobile']
                }),

        ('Adress information',{
                'fields': ['streetname', 'streetnumber', 'zipcode',
                           'city', 'country']
                }),

        ('Science information',{
                 'fields': ['position', 'office', 'work_phone',
                             'ads_name', 'research', 'contact']
                }),

        ('Extra information',{
                'classes': ['collapse'],
                'fields': ['comments']
                }),
    ]

    class Media:
        js = ADMIN_MEDIA_JS


admin.site.register(Alumnus, AlumnusAdmin)
