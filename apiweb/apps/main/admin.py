from django.contrib import admin
from .models import Sticky
from ...settings import ADMIN_MEDIA_JS


class StickyAdmin(admin.ModelAdmin):

    list_display = ('title', 'visible')

    class Media:
        js = ADMIN_MEDIA_JS + ('javascript/admin/news.js',)


# admin.site.register(Sticky, StickyAdmin)
