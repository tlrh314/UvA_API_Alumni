from django.contrib import admin
from .models import Person, Job, MastersDegree, PhdDegree, PostdocPosition


class JobAdminInline(admin.StackedInline):
    model = Job
    extra = 1
    fieldsets = [
    ('Job information',
        {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
        )
    ]


class MastersDegreeAdminInline(admin.StackedInline):
    model = MastersDegree
    max_num = 1
    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]

class PhdDegreeAdminInline(admin.StackedInline):
    model = PhdDegree
    max_num = 1
    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]


class PostdocPositionAdminInline(admin.StackedInline):
    model = PostdocPosition
    max_num = 1
    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]

class PersonAdmin(admin.ModelAdmin):
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
                             'place_of_birth','nationality', 'mugshot',
                              'photo','biography']
                }),

        ('Contact information',{
                'fields':['linkedin','facebook','email','home_phone','homepage','mobile']
                }),

        ('Adress information',{
                'fields': ['streetname', 'streetnumber', 'zipcode', 'city', 'country']
                }),

        ('Science information',{
                 'fields': ['position', 'office', 'work_phone',
                             'ads_name', 'research', 'contact']
                }),

        ('Extra information',{
                'classes': ['collapse'],
                'fields': ['comments']
                }),

        # ('Jobs',{
        #         'fields': ['jobs']
        #         }),
    ]

admin.site.register(Person, PersonAdmin)
#admin.site.register(Job, PersonAdmin)

