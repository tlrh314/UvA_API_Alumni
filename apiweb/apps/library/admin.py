from __future__ import unicode_literals, absolute_import, division

from django.contrib import admin
from .models import BookCategory, Book, PhDThesis, Proceeding


class BookCategoryAdmin(admin.ModelAdmin):

    list_filter = ('category',)
    list_display = ('category',)
    search_fields = ('category',)
    fields = ('category',)


class BookAdmin(admin.ModelAdmin):

    list_filter = ('status',)
    list_display = ('label', 'authors', 'title', 'status')
    search_fields = ('label', 'authors', 'title', 'year', 'status')
    ordering = ('label',)
    fields = ('authors', 'title', 'year', 'label', 'status', 'category')


class ProceedingAdmin(admin.ModelAdmin):

    list_filter = ('status',)
    list_display = ('authors', 'title', 'year', 'status')
    search_fields = ('authors', 'title', 'year', 'status')
    ordering = ('-year',)
    fields = ('authors', 'title', 'year', 'label', 'status')


class PhDThesisAdmin(admin.ModelAdmin):

    list_filter = ('status',)
    list_display = ('author', 'title', 'year', 'status')
    search_fields = ('author', 'title', 'year', 'status')
    ordering = ('-year',)
    fields = ('author', 'title', 'year', 'university', 'status')


admin.site.register(Book, BookAdmin)
admin.site.register(PhDThesis, PhDThesisAdmin)
admin.site.register(Proceeding, ProceedingAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)
