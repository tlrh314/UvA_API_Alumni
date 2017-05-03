from __future__ import unicode_literals, absolute_import, division
import copy

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django.contrib.auth.models import User

from tinymce.widgets import TinyMCE
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Alumnus, Job, MastersDegree, PhdDegree, PostdocPosition, MasterThesis, PhdThesis
from ...settings import ADMIN_MEDIA_JS, TINYMCE_MINIMAL_CONFIG



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
    filter_horizontal = ('supervisor',)


class PhdThesisInline(NestedStackedInline):
    model = PhdThesis
    extra = 1
    filter_horizontal = ('supervisor',)


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


# Cannot register MastersDegreeAdminInline for MastersDegree
# When doing so this raises the following error
# AttributeError: 'MastersDegreeAdmin' object has no attribute 'urls'
# TODO: check why this is, and see how we can avoid defining two
# separate classes to inline MasterThesis in Alumnus and in MasterDegre
@admin.register(MastersDegree)
class MastersDegreeAdmin(admin.ModelAdmin):
    model = MastersDegree
    max_num = 1
    inlines = (MasterThesisInline,)

    list_display = ('get_alumnus', 'get_title', )

    def get_alumnus(self, obj):
        return obj.alumnus.full_name
    get_alumnus.short_description = 'Alumnus'

    def get_title(self, obj):
        return obj.msc_thesis.title
    get_title.short_description = "Master's Thesis Title"


@admin.register(PhdDegree)
class PhdDegreeAdmin(admin.ModelAdmin):
    model = PhdDegree
    max_num = 1
    inlines = (PhdThesisInline,)

    list_display = ('get_alumnus', 'get_title', )

    def get_alumnus(self, obj):
        return obj.alumnus.full_name
    get_alumnus.short_description = 'Alumnus'

    def get_title(self, obj):
        return obj.phd_thesis.title
    get_title.short_description = 'PhD Thesis Title'


@admin.register(PhdThesis)
class PhdThesisAdmin(admin.ModelAdmin):
    model = PhdThesis

    list_display = ("get_alumnus", "title", )
    filter_horizontal = ( "supervisor", )

    def get_alumnus(self, obj):
        return obj.degree.alumnus.full_name
    get_alumnus.short_description = 'Alumnus'

    def get_title(self, obj):
        return obj.phd_thesis.title
    get_title.short_description = 'PhD Thesis Title'


@admin.register(MasterThesis)
class MasterThesisAdmin(admin.ModelAdmin):
    model = MastersDegree

    list_display = ("get_alumnus", "title", )
    filter_horizontal = ( "supervisor", )

    def get_alumnus(self, obj):
        return obj.degree.alumnus.full_name
    get_alumnus.short_description = 'Alumnus'

    def get_title(self, obj):
        return obj.msc_thesis.title
    get_title.short_description = "Master's Thesis Title"


class PostdocPositionAdminInline(NestedStackedInline):
    model = PostdocPosition
    max_num = 1

    # fieldsets = [
    # ('Job information',
    #     {'fields':['position_name','current_job','company_name','start_date','stop_date','inside_academia','location_job']}
    #     )
    # ]

class UserRawIdWidget(widgets.ForeignKeyRawIdWidget):
    """ Class to replace alumnus.user from dropdown to pk /w filter """
    def url_parameters(self):
        res = super(UserRawIdWidget, self).url_parameters()
        object = self.attrs.get('object', None)
        if object:
            res['username__exact'] = object.user.username
        return res


class AlumnusAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Init is only defined to for UserRawIdWidget """
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        obj = kwargs.get('instance', None)
        if obj and obj.pk is not None:
            self.fields['user'].widget = UserRawIdWidget(
                rel=obj._meta.get_field('user').rel,
                admin_site=admin.site,
                # Pass the object to attrs
                attrs={'object': obj}
            )

    # Change biography to TinyMCE field
    look = copy.copy(TINYMCE_MINIMAL_CONFIG)
    look['width'] = ''
    look['height'] = '200'
    biography = forms.CharField(widget=TinyMCE(mce_attrs=look))

    class Meta:
        fields = '__all__'
        model = Alumnus


@admin.register(Alumnus)
class AlumnusAdmin(NestedModelAdmin):
    list_filter = ('show_person', 'position')
    list_display = ('user','email','show_person', 'first_name', 'prefix', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('user__username',)
    inlines = (JobAdminInline, MastersDegreeAdminInline,
        PhdDegreeAdminInline, PostdocPositionAdminInline)
    # exclude = ('jobs',)

    form = AlumnusAdminForm
    filter_horizontal = ('research', 'contact', )


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
                'fields': ['address', 'streetname', 'streetnumber', 'zipcode',
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


admin.site.register(Job)
admin.site.register(PostdocPosition)
